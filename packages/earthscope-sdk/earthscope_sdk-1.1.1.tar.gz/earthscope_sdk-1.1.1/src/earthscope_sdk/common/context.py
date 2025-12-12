import sys
from functools import cached_property
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Optional, TypeVar, cast

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec


if TYPE_CHECKING:
    from httpx import AsyncClient

    from earthscope_sdk.common._sync_runner import SyncRunner
    from earthscope_sdk.config.settings import SdkSettings

T_Retval = TypeVar("T_Retval")
T_ParamSpec = ParamSpec("T_ParamSpec")


class SdkContext:
    """
    Shared context for the EarthScope SDK
    """

    @cached_property
    def auth_flow(self):
        """
        Reusable AuthFlow instance for managing token lifecycle
        """
        # lazy import; avoid circular dependency
        from earthscope_sdk.auth.auth_flow import AuthFlow
        from earthscope_sdk.config.models import AuthFlowType

        auth_flow_type = self.settings.oauth2.auth_flow_type

        if auth_flow_type == AuthFlowType.DeviceCode:
            return cast(AuthFlow, self.device_code_flow)

        if auth_flow_type == AuthFlowType.MachineToMachine:
            return cast(AuthFlow, self.client_credentials_flow)

        # Fall back to base auth flow; if a refresh token is present, we can still
        # facilitate automated renewal.
        return AuthFlow(ctx=self)

    @cached_property
    def client_credentials_flow(self):
        """
        Reusable ClientCredentialsFlow instance for managing token lifecycle
        """
        # lazy import; avoid circular dependency
        from earthscope_sdk.auth.client_credentials_flow import ClientCredentialsFlow

        return ClientCredentialsFlow(ctx=self)

    @cached_property
    def device_code_flow(self):
        """
        Resusable DeviceCodeFlow instance for managing token lifecycle
        """
        # lazy import; avoid circular dependency
        from earthscope_sdk.auth.device_code_flow import DeviceCodeFlow

        return DeviceCodeFlow(ctx=self)

    @cached_property
    def httpx_client(self):
        """
        Reusable HTTPx client for shared session and connection pooling.

        Automatically:
        - injects common headers (e.g. authorization, user-agent)
            - refreshes access token automatically
        """
        import httpx  # lazy import

        self._httpx_client = httpx.AsyncClient(
            auth=self.auth_flow,
            headers={
                **self.settings.http.extra_headers,
                # override anything specified via extra_headers
                "user-agent": self.settings.http.user_agent,
            },
            limits=self.settings.http.limits,
            timeout=self.settings.http.timeouts,
        )

        return self._httpx_client

    @property
    def is_closed(self):
        if (c := self._httpx_client) and not c.is_closed:
            return False

        if (r := self._runner) and not r.is_closed:
            return False

        return True

    @cached_property
    def settings(self):
        """
        Profile-specific settings merged with any configured defaults
        """
        return self._settings

    def __init__(
        self,
        settings: Optional["SdkSettings"] = None,
        *,
        runner: Optional["SyncRunner"] = None,
    ):
        # lazy import
        from earthscope_sdk.config.settings import SdkSettings

        # Local state
        self._httpx_client: Optional["AsyncClient"] = None
        self._runner: Optional["SyncRunner"] = runner
        self._settings = settings or SdkSettings()

    async def async_close(self):
        """
        Close this SdkContext to release underlying resources (e.g. connection pools)
        """
        if self._httpx_client:
            await self._httpx_client.aclose()

        if self._runner:
            self._runner.stop()

    def close(self):
        """
        Close this SdkContext to release underlying resources (e.g. connection pools)
        """
        # needs a different implementation than async_close()

        # need to run aclose() in the event loop
        if self._httpx_client:
            self.syncify(self._httpx_client.aclose)()

        # closing the event loop should be done *outside* the event loop *after* all async cleanup
        if self._runner:
            self._runner.stop()

    def syncify(
        self,
        async_function: Callable[T_ParamSpec, Coroutine[Any, Any, T_Retval]],
    ) -> Callable[T_ParamSpec, T_Retval]:
        """
        Create a synchronous version of an async function
        """
        if not self._runner:
            self._runner = self._get_runner()

        return self._runner.syncify(async_function)

    def _get_runner(self) -> "SyncRunner":
        # lazy imports
        import asyncio

        from earthscope_sdk.common._sync_runner import (
            BackgroundSyncRunner,
            SimpleSyncRunner,
        )

        try:
            asyncio.get_running_loop()

        except RuntimeError:
            # No event loop exists in this thread; we can run in this thread
            return SimpleSyncRunner()

        else:
            # An event loop already exists in this thread; create a background thread
            return BackgroundSyncRunner()
