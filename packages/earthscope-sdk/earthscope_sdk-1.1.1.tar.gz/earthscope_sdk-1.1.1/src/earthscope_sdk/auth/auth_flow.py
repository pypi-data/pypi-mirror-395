import datetime as dt
import logging
from contextlib import suppress
from typing import Optional

import httpx
from pydantic import ValidationError

from earthscope_sdk.auth.error import (
    InvalidRefreshTokenError,
    NoAccessTokenError,
    NoRefreshTokenError,
    NoTokensError,
)
from earthscope_sdk.common.context import SdkContext
from earthscope_sdk.config.models import AccessTokenBody, Tokens

logger = logging.getLogger(__name__)


class AuthFlow(httpx.Auth):
    """
    Generic oauth2 flow class for handling retrieving, validating, saving, and refreshing access tokens.
    """

    @property
    def access_token(self):
        """
        Access token

        Raises:
            NoTokensError: no tokens (at all) are present
            NoAccessTokenError: no access token is present
        """
        if at := self.tokens.access_token:
            return at.get_secret_value()

        raise NoAccessTokenError("No access token was found. Please re-authenticate.")

    @property
    def access_token_body(self):
        """
        Access token body

        Raises:
            NoAccessTokenError: no access token is present
        """
        if body := self._access_token_body:
            return body

        raise NoAccessTokenError("No access token was found. Please re-authenticate.")

    @property
    def expires_at(self):
        """
        Time of access token expiration

        Raises:
            NoAccessTokenError: no access token is present
        """
        return self.access_token_body.expires_at

    @property
    def has_refresh_token(self):
        """
        Whether or not we have a refresh token
        """
        try:
            return self.refresh_token is not None
        except NoTokensError:
            return False

    @property
    def issued_at(self):
        """
        Time of access token creation

        Raises:
            NoAccessTokenError: no access token is present
        """
        return self.access_token_body.issued_at

    @property
    def refresh_token(self):
        """
        Refresh token

        Raises:
            NoTokensError: no tokens (at all) are present
            NoRefreshTokenError: no refresh token is present
        """
        if rt := self.tokens.refresh_token:
            return rt.get_secret_value()

        raise NoRefreshTokenError("No refresh token was found. Please re-authenticate.")

    @property
    def scope(self):
        """
        Access token scope

        Raises:
            NoAccessTokenError: no access token is present
        """
        return set(self.access_token_body.scope.split())

    @property
    def tokens(self):
        """
        Oauth2 tokens managed by this auth flow

        Raises:
            NoTokensError: no tokens (at all) are present
        """
        if tokens := self._tokens:
            return tokens

        raise NoTokensError("No tokens were found. Please re-authenticate.")

    @property
    def ttl(self):
        """
        Access token time-to-live (ttl) before expiration

        Raises:
            NoAccessTokenError: no access token is present
        """
        return self.access_token_body.ttl

    def __init__(self, ctx: SdkContext) -> None:
        self._ctx = ctx
        self._settings = ctx.settings.oauth2

        # Local state
        self._access_token_body: Optional[AccessTokenBody] = None
        self._tokens: Optional[Tokens] = None

        # httpx.Auth objects can be used in either sync or async clients so we
        # facilitate both from the same class
        self.refresh = ctx.syncify(self.async_refresh)
        self.refresh_if_necessary = ctx.syncify(self.async_refresh_if_necessary)
        self.revoke_refresh_token = ctx.syncify(self.async_revoke_refresh_token)

        # Initialize with provided tokens
        with suppress(ValidationError):
            self._validate_tokens(self._settings)

    async def async_refresh(self, scope: Optional[str] = None):
        """
        Refresh the access token

        Args:
            scope: the specific oauth2 scopes to request

        Raises:
            NoTokensError: no tokens (at all) are present
            NoRefreshTokenError: no refresh token is present
            InvalidRefreshTokenError: the token refresh failed
        """
        from httpx import HTTPStatusError, ReadTimeout

        refresh_token = self.refresh_token
        scope = scope or self._settings.scope

        request = self._ctx.httpx_client.build_request(
            "POST",
            f"{self._settings.domain}oauth/token",
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "client_id": self._settings.client_id,
                "refresh_token": refresh_token,
                "scopes": scope,
            },
        )

        try:
            async for attempt in self._settings.retry.retry_context(ReadTimeout):
                with attempt:
                    r = await self._ctx.httpx_client.send(request, auth=None)
                    r.raise_for_status()
        except HTTPStatusError as e:
            logger.error(
                f"error during token refresh ({attempt.num} attempts): {e.response.content}"
            )
            raise InvalidRefreshTokenError("refresh token exchange failed")
        except Exception as e:
            logger.error(
                f"error during token refresh ({attempt.num} attempts)", exc_info=e
            )
            raise InvalidRefreshTokenError("refresh token exchange failed") from e

        # add previous refresh token to new tokens if omitted from resp
        # (i.e. we have a non-rotating refresh token)
        resp: dict = r.json()
        resp.setdefault("refresh_token", refresh_token)

        self._validate_and_save_tokens(resp)

        logger.debug(f"Refreshed tokens: {self._tokens}")
        return self

    async def async_refresh_if_necessary(
        self,
        scope: Optional[str] = None,
        auto_refresh_threshold: int = 60,
    ):
        """
        Refresh the access token if it is expired or bootstrap the access token from a refresh token

        Args:
            scope: the specific oauth2 scopes to request
            auto_refresh_threshold: access token TTL remaining (in seconds) before auto-refreshing

        Raises:
            NoTokensError: no tokens (at all) are present
            NoRefreshTokenError: no refresh token is present
            InvalidRefreshTokenError: the token refresh failed
        """
        # Suppress to allow bootstrapping with a refresh token
        with suppress(NoAccessTokenError):
            if self.ttl >= dt.timedelta(seconds=auto_refresh_threshold):
                return self

        return await self.async_refresh(scope=scope)

    async def async_revoke_refresh_token(self):
        """
        Revoke the refresh token.

        This invalidates the refresh token server-side so it may never again be used to
        get new access tokens.

        Raises:
            NoTokensError: no tokens (at all) are present
            NoRefreshTokenError: no refresh token is present
            InvalidRefreshTokenError: the token revocation failed
        """
        refresh_token = self.refresh_token

        r = await self._ctx.httpx_client.post(
            f"{self._settings.domain}oauth/revoke",
            auth=None,  # override client default
            headers={"content-type": "application/json"},
            json={
                "client_id": self._settings.client_id,
                "token": refresh_token,
            },
        )

        if r.status_code != 200:
            logger.error(f"error while revoking refresh token: {r.content}")
            raise InvalidRefreshTokenError("refresh token revocation failed")

        logger.debug(f"Refresh token revoked: {refresh_token}")
        return self

    def _validate_and_save_tokens(self, unvalidated_tokens: dict):
        """
        Validate then save tokens to local storage

        Args:
            unvalidated_tokens: tokens that have yet to be validated

        Returns:
            this auth flow

        Raises:
            pydantic.ValidationError: the token's body could not be decoded
        """
        self._validate_tokens(unvalidated_tokens)

        try:
            self._ctx.settings.write_tokens(self._tokens)
        except Exception as e:
            logger.error("Error while persisting tokens", exc_info=e)
            raise

        return self

    def _validate_tokens(self, unvalidated_tokens: dict):
        """
        Validate the tokens

        Args:
            unvalidated_tokens: tokens that have yet to be validated

        Returns:
            this auth flow

        Raises:
            pydantic.ValidationError: the token's body could not be decoded
        """

        tokens = Tokens.model_validate(unvalidated_tokens)

        self._access_token_body = tokens.access_token_body
        self._tokens = tokens

        return self

    ##########
    # The following methods make this class compatible with httpx.Auth.
    ##########

    async def async_auth_flow(self, request: httpx.Request):
        """
        Injects authorization into the request

        (this method makes this class httpx.Auth compatible)
        """
        super().async_auth_flow
        if request.headers.get("authorization") is None:
            if self._settings.is_host_allowed(request.url.host):
                await self.async_refresh_if_necessary()
                access_token = self.access_token
                request.headers["authorization"] = f"Bearer {access_token}"

        yield request

    def sync_auth_flow(self, request: httpx.Request):
        """
        Injects authorization into the request

        (this method makes this class httpx.Auth compatible)
        """
        # NOTE: we explicitly redefine this sync method because ctx.syncify()
        # does not support generators
        if request.headers.get("authorization") is None:
            if self._settings.is_host_allowed(request.url.host):
                self.refresh_if_necessary()
                access_token = self.access_token
                request.headers["authorization"] = f"Bearer {access_token}"

        yield request
