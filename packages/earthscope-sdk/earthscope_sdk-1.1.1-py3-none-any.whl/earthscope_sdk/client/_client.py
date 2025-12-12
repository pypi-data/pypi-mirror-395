from functools import cached_property

from earthscope_sdk.common.client import AsyncSdkClient, SdkClient


class AsyncEarthScopeClient(AsyncSdkClient):
    """
    An async client for interacting with api.earthscope.org
    """

    @cached_property
    def user(self):
        """
        User and Identity Management functionality
        """
        # lazy load
        from earthscope_sdk.client.user._service import AsyncUserService

        return AsyncUserService(self._ctx)


class EarthScopeClient(SdkClient):
    """
    A client for interacting with api.earthscope.org
    """

    @cached_property
    def user(self):
        """
        User and Identity Management functionality
        """
        # lazy load
        from earthscope_sdk.client.user._service import UserService

        return UserService(self._ctx)
