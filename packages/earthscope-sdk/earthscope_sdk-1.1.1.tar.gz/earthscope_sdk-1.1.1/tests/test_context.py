import warnings

import httpx
import pytest
from pytest_httpx import HTTPXMock

from earthscope_sdk.auth.error import NoAccessTokenError
from earthscope_sdk.common.context import SdkContext
from earthscope_sdk.config.models import HttpSettings
from earthscope_sdk.config.settings import SdkSettings


class TestContext:
    @pytest.mark.parametrize(
        "host",
        [
            "earthscope.org",
            "api.earthscope.org",
            "data.earthscope.org",
        ],
    )
    @pytest.mark.asyncio
    async def test_context_async_refreshes_and_injects_auth_header_for_allowed_hosts(
        self,
        mock_settings: SdkSettings,
        httpx_mock: HTTPXMock,
        host: str,
    ):
        httpx_mock.add_response()

        ctx = SdkContext(mock_settings)
        with pytest.raises(NoAccessTokenError):
            ctx.auth_flow.access_token

        await ctx.httpx_client.get(f"https://{host}/foo")

        at = ctx.auth_flow.access_token
        req = httpx_mock.get_requests()

        assert req[1].url.host == host
        assert req[1].headers["authorization"] == f"Bearer {at}"
        assert req[1].headers["user-agent"] == mock_settings.http.user_agent

    @pytest.mark.parametrize(
        "host",
        [
            "foo.org",
            "earthscope.foo.org",
        ],
    )
    @pytest.mark.httpx_mock(assert_all_responses_were_requested=False)
    @pytest.mark.asyncio
    async def test_context_allowed_hosts_doesnt_inject_auth_header(
        self,
        mock_settings: SdkSettings,
        httpx_mock: HTTPXMock,
        host: str,
    ):
        httpx_mock.add_response()

        ctx = SdkContext(mock_settings)
        with pytest.raises(NoAccessTokenError):
            ctx.auth_flow.access_token

        await ctx.httpx_client.get(f"https://{host}/bar")

        with pytest.raises(NoAccessTokenError):
            ctx.auth_flow.access_token

        req = httpx_mock.get_requests()

        assert req[0].url.host == host
        assert req[0].headers["user-agent"] == mock_settings.http.user_agent
        with pytest.raises(KeyError):
            req[0].headers["authorization"]

    @pytest.mark.asyncio
    async def test_context_async_close(
        self,
        mock_settings: SdkSettings,
        httpx_mock: HTTPXMock,
    ):
        httpx_mock.add_response(text="OK")
        ctx = SdkContext(mock_settings)

        async def async_foo():
            return await ctx.httpx_client.get(f"{mock_settings.resources.api_url}foo")

        foo = ctx.syncify(async_foo)
        resp = foo()
        assert resp.text == "OK"

        assert not ctx.is_closed
        await ctx.async_close()

        assert ctx._httpx_client.is_closed
        assert ctx._runner.is_closed
        assert ctx.is_closed

        # can no longer schedule
        with warnings.catch_warnings(), pytest.raises(RuntimeError):
            warnings.filterwarnings(
                "ignore",
                message=r"coroutine '.+' was never awaited",
            )
            foo()

    def test_context_sync_close(
        self,
        mock_settings: SdkSettings,
        httpx_mock: HTTPXMock,
    ):
        httpx_mock.add_response(text="OK")
        ctx = SdkContext(mock_settings)

        async def async_foo():
            return await ctx.httpx_client.get(f"{mock_settings.resources.api_url}foo")

        foo = ctx.syncify(async_foo)
        resp = foo()
        assert resp.text == "OK"

        assert not ctx.is_closed
        ctx.close()

        assert ctx._httpx_client.is_closed
        assert ctx._runner.is_closed
        assert ctx.is_closed

        # can no longer schedule
        with warnings.catch_warnings(), pytest.raises(RuntimeError):
            warnings.filterwarnings(
                "ignore",
                message=r"coroutine '.+' was never awaited",
            )
            foo()

    def test_auth_flow_in_custom_sync_client(
        self,
        mock_settings: SdkSettings,
        httpx_mock: HTTPXMock,
    ):
        httpx_mock.add_response()

        ctx = SdkContext(mock_settings)
        with pytest.raises(NoAccessTokenError):
            ctx.auth_flow.access_token

        with httpx.Client(auth=ctx.auth_flow) as c:
            c.get(f"{mock_settings.resources.api_url}foo")

        at = ctx.auth_flow.access_token
        req = httpx_mock.get_requests()

        assert str(req[1].url).startswith(f"{mock_settings.resources.api_url}")
        assert req[1].headers["authorization"] == f"Bearer {at}"

        # note: in custom client, we don't expect our custom user-agent
        assert req[1].headers["user-agent"] != mock_settings.http.user_agent

    def test_extra_headers_injected_into_requests(self):
        settings = SdkSettings(
            http=HttpSettings(
                user_agent="aaa-user-agent",
                extra_headers={
                    "x-test-header": "test",
                    "user-agent": "bbb-user-agent",
                },
            ),
        )

        ctx = SdkContext(settings)
        req = ctx.httpx_client.build_request("GET", "https://www.foo.com")

        assert req.headers["x-test-header"] == "test", "extra header injected"
        assert req.headers["user-agent"] == "aaa-user-agent", "user-agent override"
