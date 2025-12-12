import logging
from json import JSONDecodeError

from earthscope_sdk.auth.auth_flow import AuthFlow
from earthscope_sdk.auth.error import ClientCredentialsFlowError, UnauthorizedError
from earthscope_sdk.common.context import SdkContext

logger = logging.getLogger(__name__)


class ClientCredentialsFlow(AuthFlow):
    """
    Implements the oauth2 Client Credentials "machine-to-machine" (M2M) flow.
    """

    def __init__(self, ctx: SdkContext):
        if not ctx.settings.oauth2.client_secret:
            raise ValueError("Client secret required for client credentials flow")

        super().__init__(ctx=ctx)

        # httpx.Auth objects can be used in either sync or async clients so we
        # facilitate both from the same class
        self.request_tokens = ctx.syncify(self.async_request_tokens)

    async def async_refresh(self, *args, **kwargs):
        # alias for self.request_tokens() so that base class can get new tokens automagically
        return await self.async_request_tokens()

    async def async_request_tokens(self):
        """
        Request access token from IdP

        Raises:
            Unauthorized Error: the request returns as unauthorized
            ClientCredentialsFlowError: unhandled error in the client credentials flow
        """
        r = await self._ctx.httpx_client.post(
            f"{self._settings.domain}oauth/token",
            auth=None,  # override client default
            headers={"content-type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": self._settings.client_id,
                "client_secret": self._settings.client_secret.get_secret_value(),
                "audience": self._settings.audience,
            },
        )
        try:
            resp: dict = r.json()
        except JSONDecodeError:
            raise ClientCredentialsFlowError(
                f"Unable to unpack IdP response: {r.content}"
            )

        # Success!
        if r.status_code == 200:
            self._validate_and_save_tokens(resp)

            logger.debug(f"Got tokens: {self.tokens}")
            return self

        # Unauthorized
        if r.status_code == 401:
            raise UnauthorizedError(
                f"m2m client '{self._settings.client_id}' is not authorized. IdP response: {resp}"
            )

        # Unhandled
        raise ClientCredentialsFlowError("client credentials flow failed", r.content)
