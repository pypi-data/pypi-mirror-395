from typing import TYPE_CHECKING

from earthscope_sdk.auth.error import UnauthenticatedError, UnauthorizedError

if TYPE_CHECKING:
    from httpx import Request

    from earthscope_sdk.common.context import SdkContext


class SdkService:
    """
    Base class for EarthScope SDK services
    """

    @property
    def ctx(self):
        """
        SDK Context
        """
        return self._ctx

    @property
    def resources(self):
        """
        References to EarthScope resources
        """
        return self.ctx.settings.resources

    def __init__(self, ctx: "SdkContext"):
        self._ctx = ctx

    async def _send(self, request: "Request"):
        """
        Send an HTTP request.

        Performs common response handling.
        """
        resp = await self.ctx.httpx_client.send(request=request)

        # Throw specific errors for certain status codes

        if resp.status_code == 401:
            await resp.aread()  # must read body before using .text prop
            raise UnauthenticatedError(resp.text)

        if resp.status_code == 403:
            await resp.aread()  # must read body before using .text prop
            raise UnauthorizedError(resp.text)

        # Raise HTTP errors
        resp.raise_for_status()

        return resp

    async def _send_with_retries(self, request: "Request"):
        async for attempt in self.ctx.settings.http.retry.retry_context():
            with attempt:
                return await self._send(request=request)
