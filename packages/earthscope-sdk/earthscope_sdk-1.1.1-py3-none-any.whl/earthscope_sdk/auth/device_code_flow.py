import logging
from asyncio import sleep
from contextlib import asynccontextmanager, contextmanager
from enum import Enum
from json import JSONDecodeError
from typing import Optional

from pydantic import BaseModel, ValidationError

from earthscope_sdk.auth.auth_flow import AuthFlow
from earthscope_sdk.auth.error import (
    DeviceCodePollingError,
    DeviceCodePollingExpiredError,
    DeviceCodeRequestDeviceCodeError,
    UnauthorizedError,
)
from earthscope_sdk.common.context import SdkContext

logger = logging.getLogger(__name__)


class PollingErrorType(str, Enum):
    AUTHORIZATION_PENDING = "authorization_pending"
    SLOW_DOWN = "slow_down"
    EXPIRED_TOKEN = "expired_token"
    ACCESS_DENIED = "access_denied"


class GetDeviceCodeResponse(BaseModel):
    device_code: str
    user_code: str
    verification_uri: str
    verification_uri_complete: str
    expires_in: int
    interval: float


class PollingErrorResponse(BaseModel):
    error: PollingErrorType
    error_description: str


class DeviceCodeFlow(AuthFlow):
    """
    Implements the oauth2 Device Code flow.
    """

    @property
    def polling(self):
        """
        This instance is in the process of polling for tokens
        """
        return self._is_polling

    def __init__(self, ctx: SdkContext):
        if ctx.settings.oauth2.client_secret:
            raise ValueError("Client secret should not be used with device code flow")

        super().__init__(ctx=ctx)

        # Flow management vars
        self._is_polling = False

        # httpx.Auth objects can be used in either sync or async clients so we
        # facilitate both from the same class
        self._poll = ctx.syncify(self._async_poll)
        self._request_device_code = ctx.syncify(self._async_request_device_code)

    @asynccontextmanager
    async def async_do_flow(self, scope: Optional[str] = None):
        """
        Perform the oauth2 Device Code flow:
        - requests device code
        - yields the device code to the caller for them to prompt the user
        - polls for access token

        Args:
            scope: the specific oauth2 scopes to request

        Yields:
            GetDeviceCodeResponse: the device code response that must be shown to the user
                to facilitate a login.

        Raises:
            DeviceCodeRequestDeviceCodeError: failed to get a device code from the IdP
            DeviceCodePollingExpiredError: the polling token expired
            UnauthorizedError: access denied
            DeviceCodePollingError: unhandled polling error

        Examples:
            >>> async with device_flow.async_do_flow() as codes:
            ...     # prompt the user to login using the device code
            ...     print(f"Open the following URL in a web browser to login: {codes.verification_uri_complete}")
        """
        # NOTE: if you update this method, also update the synchronous version

        codes = await self._async_request_device_code(scope=scope)

        # Yield codes to facilitate prompting the user
        yield codes

        await self._async_poll(codes=codes)

    @contextmanager
    def do_flow(self, scope: Optional[str] = None):
        """
        Perform the oauth2 Device Code flow:
        - requests device code
        - yields the device code to the caller for them to prompt the user
        - polls for access token

        Args:
            scope: the specific oauth2 scopes to request

        Yields:
            GetDeviceCodeResponse: the device code response that must be shown to the user
                to facilitate a login.

        Raises:
            DeviceCodeRequestDeviceCodeError: failed to get a device code from the IdP
            DeviceCodePollingExpiredError: the polling token expired
            UnauthorizedError: access denied
            DeviceCodePollingError: unhandled polling error

        Examples:
            >>> with device_flow.do_flow() as codes:
            ...     # prompt the user to login using the device code
            ...     print(f"Open the following URL in a web browser to login: {codes.verification_uri_complete}")
        """
        # NOTE: we explicitly redefine this sync method because ctx.syncify()
        # does not support generators

        codes = self._request_device_code(scope=scope)

        # Yield codes to facilitate prompting the user
        yield codes

        self._poll(codes=codes)

    async def _async_poll(self, codes: GetDeviceCodeResponse):
        """
        Polling IdP for tokens.

        Args:
            codes: device code response from IdP after starting the flow

        Raises:
            DeviceCodePollingExpiredError: the polling token expired
            UnauthorizedError: access denied
            DeviceCodePollingError: unhandled polling error
        """
        if self._is_polling:
            raise DeviceCodePollingError("Polling is already in progress")

        self._is_polling = True
        try:
            while True:
                # IdP-provided poll interval
                await sleep(codes.interval)

                r = await self._ctx.httpx_client.post(
                    f"{self._settings.domain}oauth/token",
                    auth=None,  # override client default
                    headers={"content-type": "application/x-www-form-urlencoded"},
                    data={
                        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                        "device_code": codes.device_code,
                        "client_id": self._settings.client_id,
                    },
                )

                try:
                    resp: dict = r.json()
                except JSONDecodeError:
                    raise DeviceCodePollingError(
                        f"Unable to unpack IdP response: {r.content}"
                    )

                # Success!
                if r.status_code == 200:
                    self._validate_and_save_tokens(resp)

                    logger.debug(f"Got tokens: {self.tokens}")
                    return self

                # Keep polling
                try:
                    poll_err = PollingErrorResponse.model_validate(resp)
                except ValidationError as e:
                    raise DeviceCodePollingError(
                        f"Failed to unpack polling response: {r.text}"
                    ) from e
                if poll_err.error in [
                    PollingErrorType.AUTHORIZATION_PENDING,
                    PollingErrorType.SLOW_DOWN,
                ]:
                    continue

                # Timeout
                if poll_err.error == PollingErrorType.EXPIRED_TOKEN:
                    raise DeviceCodePollingExpiredError

                # Unauthorized
                if poll_err.error == PollingErrorType.ACCESS_DENIED:
                    raise UnauthorizedError

                # Unhandled
                if poll_err:
                    raise DeviceCodePollingError(f"Unknown polling error: {poll_err}")

        finally:
            self._is_polling = False

    async def _async_request_device_code(self, scope: Optional[str] = None):
        """
        Request new device code from IdP

        Args:
            scope: the specific oauth2 scopes to request

        Raises:
            DeviceCodeRequestDeviceCodeError: failed to get a device code from the IdP
        """
        scope = scope or self._settings.scope

        r = await self._ctx.httpx_client.post(
            f"{self._settings.domain}oauth/device/code",
            auth=None,  # override client default
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "client_id": self._settings.client_id,
                "scope": scope,
                "audience": self._settings.audience,
            },
        )

        if r.status_code != 200:
            raise DeviceCodeRequestDeviceCodeError(
                f"Failed to get a device code: {r.content}"
            )

        try:
            codes = GetDeviceCodeResponse.model_validate_json(r.content)
        except ValidationError as e:
            raise DeviceCodeRequestDeviceCodeError(
                f"Failed to unpack device code response: {r.text}"
            ) from e

        logger.debug(f"Got device code response: {codes}")
        return codes
