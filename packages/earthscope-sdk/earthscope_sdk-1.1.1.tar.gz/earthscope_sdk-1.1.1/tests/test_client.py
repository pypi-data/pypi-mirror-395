import datetime as dt

import pytest
from pytest_httpx import HTTPXMock

from earthscope_sdk.auth.error import NoAccessTokenError
from earthscope_sdk.client import AsyncEarthScopeClient, EarthScopeClient
from earthscope_sdk.client.user.models import AwsTemporaryCredentials, UserProfile
from earthscope_sdk.common.context import SdkContext
from earthscope_sdk.config.settings import SdkSettings
from tests.util import retries_enabled


class TestSyncClient:
    def test_sdk_auto_injects_auth_header(
        self,
        mock_settings: SdkSettings,
        httpx_mock: HTTPXMock,
    ):
        u = UserProfile(
            first_name="Jane",
            last_name="Doe",
            country_code="US",
            region_code="CO",
            institution="EarthScope Consortium",
            work_sector="non-profit",
            user_id="user-id-123",
            primary_email="jane.doe@earthscope.org",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-03-01T00:00:00Z",
        )
        httpx_mock.add_response(json=u.model_dump(mode="json"))

        with EarthScopeClient(settings=mock_settings) as client:
            with pytest.raises(NoAccessTokenError):
                client.ctx.auth_flow.access_token

            u_resp = client.user.get_profile()

            at = client.ctx.auth_flow.access_token

        req = httpx_mock.get_requests()

        assert str(req[1].url).startswith(f"{mock_settings.resources.api_url}")
        assert req[1].headers["authorization"] == f"Bearer {at}"
        assert req[1].headers["user-agent"] == mock_settings.http.user_agent

        assert u == u_resp

        assert client.is_closed


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_sdk_auto_injects_auth_header(
        self,
        mock_settings: SdkSettings,
        httpx_mock: HTTPXMock,
    ):
        u = UserProfile(
            first_name="Jane",
            last_name="Doe",
            country_code="US",
            region_code="CO",
            institution="EarthScope Consortium",
            work_sector="non-profit",
            user_id="user-id-123",
            primary_email="jane.doe@earthscope.org",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-03-01T00:00:00Z",
        )
        httpx_mock.add_response(json=u.model_dump(mode="json"))

        async with AsyncEarthScopeClient(settings=mock_settings) as client:
            with pytest.raises(NoAccessTokenError):
                client.ctx.auth_flow.access_token

            u_resp = await client.user.get_profile()

            at = client.ctx.auth_flow.access_token

        req = httpx_mock.get_requests()

        assert str(req[1].url).startswith(f"{mock_settings.resources.api_url}")
        assert req[1].headers["authorization"] == f"Bearer {at}"
        assert req[1].headers["user-agent"] == mock_settings.http.user_agent

        assert u == u_resp

        assert client.is_closed

    @pytest.mark.asyncio
    async def test_aws_credentials_caching(
        self,
        mock_settings: SdkSettings,
        httpx_mock: HTTPXMock,
    ):
        # reuse context
        ctx = SdkContext(settings=mock_settings)

        now = dt.datetime.now(dt.timezone.utc)
        c1 = AwsTemporaryCredentials(
            aws_access_key_id="mock-access-key",
            aws_secret_access_key="mock-secret-key",
            aws_session_token="mock-session-token",
            expiration=now + dt.timedelta(hours=1),  # creds must expire in the future
        )
        httpx_mock.add_response(json=c1.model_dump(mode="json"))

        c2 = AwsTemporaryCredentials(
            aws_access_key_id="mock-access-key-refresh",
            aws_secret_access_key="mock-secret-key-refresh",
            aws_session_token="mock-session-token-refresh",
            expiration=now + dt.timedelta(hours=2),  # creds must expire in the future
        )
        httpx_mock.add_response(json=c2.model_dump(mode="json"))

        async with AsyncEarthScopeClient(ctx=ctx) as client:
            c_resp = await client.user.get_aws_credentials()
            assert c_resp == c1, "got credentials"

            c_resp = await client.user.get_aws_credentials()
            assert c_resp == c1, "memory cache hit"

        # create a new client with empty memory cache
        async with AsyncEarthScopeClient(ctx=ctx) as client:
            c_resp = await client.user.get_aws_credentials()
            assert c_resp == c1, "disk cache hit"

            c_resp = await client.user.get_aws_credentials(force=True)
            assert c_resp == c2, "got new credentials when forced"

    @pytest.mark.asyncio
    async def test_retries(
        self,
        mock_settings: SdkSettings,
        httpx_mock: HTTPXMock,
    ):
        # reuse context
        ctx = SdkContext(settings=mock_settings)

        httpx_mock.add_response(429)
        httpx_mock.add_response(429)

        u = UserProfile(
            first_name="Jane",
            last_name="Doe",
            country_code="US",
            region_code="CO",
            institution="EarthScope Consortium",
            work_sector="non-profit",
            user_id="user-id-123",
            primary_email="jane.doe@earthscope.org",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-03-01T00:00:00Z",
        )
        httpx_mock.add_response(json=u.model_dump(mode="json"))

        with retries_enabled(3):
            async with AsyncEarthScopeClient(ctx=ctx) as client:
                u_resp = await client.user.get_profile()
                assert u == u_resp
