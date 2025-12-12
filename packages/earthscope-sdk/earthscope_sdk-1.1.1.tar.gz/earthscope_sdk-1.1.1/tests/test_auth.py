import time
import webbrowser
from typing import Type

import pytest
from pytest_httpx import HTTPXMock

from earthscope_sdk.auth.client_credentials_flow import ClientCredentialsFlow
from earthscope_sdk.auth.device_code_flow import DeviceCodeFlow, PollingErrorType
from earthscope_sdk.auth.error import (
    DeviceCodePollingExpiredError,
    DeviceCodeRequestDeviceCodeError,
    NoRefreshTokenError,
    NoTokensError,
    UnauthorizedError,
)
from earthscope_sdk.client import AsyncEarthScopeClient
from earthscope_sdk.common.context import SdkContext
from earthscope_sdk.config.models import AuthFlowSettings, Tokens
from earthscope_sdk.config.settings import SdkSettings
from tests.conftest import AUDIENCE, CLIENT_ID, DOMAIN

from .util import (
    get_m2m_creds,
    get_refresh_token,
    is_pipeline,
    missing_m2m_creds,
    missing_refresh_token,
    register_mock_token_response,
    retries_enabled,
)


@pytest.fixture()
def device_flow_settings():
    return SdkSettings(
        oauth2=AuthFlowSettings(
            audience=AUDIENCE,
            domain=DOMAIN,
            client_id=CLIENT_ID,
        )
    )


@pytest.fixture()
def refresh_settings():
    return SdkSettings(
        oauth2=AuthFlowSettings(
            audience=AUDIENCE,
            domain=DOMAIN,
            client_id=CLIENT_ID,
            **get_refresh_token(),
        )
    )


@pytest.fixture()
def m2m_settings():
    return SdkSettings(
        oauth2=AuthFlowSettings(
            audience=AUDIENCE,
            domain=DOMAIN,
            **get_m2m_creds(),
        )
    )


class TestAuthDeviceCodeFlow:
    def test_no_tokens_device_code_flow(self, device_flow_settings: SdkSettings):
        flow = DeviceCodeFlow(SdkContext(device_flow_settings))

        with pytest.raises(NoTokensError):
            flow.access_token
        with pytest.raises(NoTokensError):
            flow.access_token_body
        with pytest.raises(NoTokensError):
            flow.refresh_token
        with pytest.raises(NoTokensError):
            flow.issued_at
        with pytest.raises(NoTokensError):
            flow.expires_at
        with pytest.raises(NoTokensError):
            flow.ttl
        with pytest.raises(NoTokensError):
            flow.scope

    @pytest.mark.asyncio
    async def test_device_code_request_error(self, httpx_mock: HTTPXMock):
        """Test handling of device code request errors."""
        httpx_mock.add_response(
            status_code=400,
            json={"error": "invalid_request", "error_description": "Invalid client"},
        )

        async with AsyncEarthScopeClient() as client:
            with pytest.raises(DeviceCodeRequestDeviceCodeError):
                await client.ctx.device_code_flow._async_request_device_code()

    @pytest.mark.parametrize(
        "err_code, ErrType",
        [
            (PollingErrorType.ACCESS_DENIED, UnauthorizedError),
            (PollingErrorType.EXPIRED_TOKEN, DeviceCodePollingExpiredError),
        ],
    )
    @pytest.mark.asyncio
    async def test_device_code_polling_error(
        self,
        httpx_mock: HTTPXMock,
        err_code: str,
        ErrType: Type[Exception],
    ):
        """Test handling of device code polling errors."""
        # First response for device code request
        httpx_mock.add_response(
            status_code=200,
            json={
                "device_code": "test_code",
                "user_code": "ABCD-EFGH",
                "verification_uri": "activate",
                "verification_uri_complete": "https://test.com/activate",
                "expires_in": 900,
                "interval": 0.001,
            },
        )
        # Second response for polling with error
        httpx_mock.add_response(
            status_code=400,
            json={
                "error": err_code,
                "error_description": "Pending",
            },
        )

        async with AsyncEarthScopeClient() as client:
            codes = await client.ctx.device_code_flow._async_request_device_code()

            with pytest.raises(ErrType):
                await client.ctx.device_code_flow._async_poll(codes=codes)

    @pytest.mark.skipif(
        is_pipeline(),
        reason="No user input in pipeline",
    )
    def test_login_device_code_flow(self, device_flow_settings: SdkSettings):
        flow = DeviceCodeFlow(SdkContext(device_flow_settings))

        with flow.do_flow() as code:
            webbrowser.open(code.verification_uri_complete)

        assert flow.access_token_body.audience == device_flow_settings.oauth2.audience
        assert flow.access_token_body.issuer == f"{device_flow_settings.oauth2.domain}"
        assert flow.access_token_body.scope == device_flow_settings.oauth2.scope
        assert flow.access_token_body.client_id == device_flow_settings.oauth2.client_id
        assert flow.refresh_token is not None

        raw = device_flow_settings.tokens_file.read_bytes()
        t = Tokens.model_validate_json(raw)
        assert t.access_token.get_secret_value() == flow.access_token
        assert t.refresh_token.get_secret_value() == flow.refresh_token

    @pytest.mark.skipif(
        missing_refresh_token(),
        reason="Missing refresh token",
    )
    def test_refresh_device_code_flow(self, refresh_settings: SdkSettings):
        flow = DeviceCodeFlow(SdkContext(refresh_settings))

        flow.refresh()

        at = flow.access_token
        body = flow.access_token_body
        assert flow.access_token_body.audience == refresh_settings.oauth2.audience
        assert flow.access_token_body.issuer == f"{refresh_settings.oauth2.domain}"
        assert flow.access_token_body.scope == refresh_settings.oauth2.scope
        assert flow.access_token_body.client_id == refresh_settings.oauth2.client_id
        assert (
            flow.refresh_token
            == refresh_settings.oauth2.refresh_token.get_secret_value()
        )

        time.sleep(1)

        flow.refresh()
        assert flow.access_token != at
        assert flow.access_token_body.issued_at > body.issued_at

    @pytest.mark.skipif(
        missing_refresh_token(),
        reason="Missing refresh token",
    )
    def test_refresh_if_necessary(self, refresh_settings: SdkSettings):
        flow = DeviceCodeFlow(SdkContext(refresh_settings))

        flow.refresh()

        at = flow.access_token
        time.sleep(1)

        flow.refresh_if_necessary()
        assert flow.access_token == at

    @pytest.mark.asyncio
    async def test_refresh_retry(
        self,
        httpx_mock: HTTPXMock,
    ):
        httpx_mock.add_response(429)
        httpx_mock.add_response(500)
        httpx_mock.add_response(502)
        httpx_mock.add_response(504)
        mock_token_body = register_mock_token_response(httpx_mock)

        settings = SdkSettings(
            oauth2=AuthFlowSettings(
                audience=AUDIENCE,
                domain=DOMAIN,
                refresh_token="mock-refresh-token",
            )
        )
        flow = DeviceCodeFlow(SdkContext(settings))

        with retries_enabled(5):
            await flow.async_refresh()

        assert len(httpx_mock.get_requests()) == 5
        assert flow.refresh_token == "mock-refresh-token"
        assert flow.access_token_body == mock_token_body


class TestAuthClientCredentialsFlow:
    def test_no_device_code_with_m2m_creds(self):
        settings = SdkSettings(
            oauth2=AuthFlowSettings(client_id="foo", client_secret="bar")
        )
        with pytest.raises(ValueError):
            DeviceCodeFlow(SdkContext(settings))

    def test_no_tokens_client_credentials_flow(self):
        settings = SdkSettings(
            oauth2=AuthFlowSettings(client_id="foo", client_secret="bar")
        )
        flow = ClientCredentialsFlow(SdkContext(settings))

        with pytest.raises(NoTokensError):
            flow.access_token
        with pytest.raises(NoTokensError):
            flow.access_token_body
        with pytest.raises(NoTokensError):
            flow.refresh_token
        with pytest.raises(NoTokensError):
            flow.issued_at
        with pytest.raises(NoTokensError):
            flow.expires_at
        with pytest.raises(NoTokensError):
            flow.ttl
        with pytest.raises(NoTokensError):
            flow.scope

    @pytest.mark.asyncio
    async def test_client_credentials_unauthorized(self, httpx_mock: HTTPXMock):
        settings = SdkSettings(
            oauth2=AuthFlowSettings(client_id="foo", client_secret="bar")
        )
        flow = ClientCredentialsFlow(SdkContext(settings))

        httpx_mock.add_response(status_code=401, json={})

        with pytest.raises(UnauthorizedError):
            await flow.async_request_tokens()

    @pytest.mark.skipif(
        missing_m2m_creds(),
        reason="Missing M2M credentials",
    )
    def test_login_client_credentials_flow(self, m2m_settings: SdkSettings):
        flow = ClientCredentialsFlow(SdkContext(m2m_settings))

        flow.refresh()

        assert flow.access_token_body.audience == m2m_settings.oauth2.audience
        assert flow.access_token_body.issuer == f"{m2m_settings.oauth2.domain}"
        # m2m scope depends on IdP setup
        assert flow.access_token_body.scope is not None
        assert flow.access_token_body.client_id == m2m_settings.oauth2.client_id

        with pytest.raises(NoRefreshTokenError):
            flow.refresh_token

        raw = m2m_settings.tokens_file.read_bytes()
        t = Tokens.model_validate_json(raw)
        assert t.access_token.get_secret_value() == flow.access_token
        assert t.refresh_token is None

    @pytest.mark.skipif(
        missing_m2m_creds(),
        reason="Missing M2M credentials",
    )
    def test_refresh_if_necessary(self, m2m_settings: SdkSettings):
        flow = ClientCredentialsFlow(SdkContext(m2m_settings))

        flow.refresh()

        at = flow.access_token
        time.sleep(1)

        flow.refresh_if_necessary()
        assert flow.access_token == at
