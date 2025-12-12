from typing import TYPE_CHECKING, Optional, overload

if TYPE_CHECKING:
    from earthscope_sdk.common.context import SdkContext
    from earthscope_sdk.config.settings import SdkSettings


class _SdkClient:
    @property
    def ctx(self):
        """
        SDK Context
        """
        return self._ctx

    @property
    def is_closed(self):
        """
        This client is closed
        """
        return self._ctx.is_closed

    @property
    def resources(self):
        """
        References to EarthScope resources
        """
        return self.ctx.settings.resources

    @overload
    def __init__(self): ...

    @overload
    def __init__(self, *, ctx: "SdkContext"): ...

    @overload
    def __init__(self, *, settings: "SdkSettings"): ...

    def __init__(
        self,
        *,
        ctx: Optional["SdkContext"] = None,
        settings: Optional["SdkSettings"] = None,
    ):
        # lazy imports
        from earthscope_sdk.common.context import SdkContext
        from earthscope_sdk.config.settings import SdkSettings

        if ctx:
            self._created_ctx = False

        else:
            if settings is None:
                settings = SdkSettings()

            ctx = SdkContext(settings=settings)
            self._created_ctx = True

        self._ctx = ctx


class AsyncSdkClient(_SdkClient):
    """
    Base class for asynchronous EarthScope SDK clients
    """

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb):
        await self.close()

    async def close(self):
        """
        Close this client
        """
        # only close the context if we created it
        if self._created_ctx:
            await self.ctx.async_close()


class SdkClient(_SdkClient):
    """
    Base class for synchronous EarthScope SDK clients
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Close this client
        """
        # only close the context if we created it
        if self._created_ctx:
            self.ctx.close()
