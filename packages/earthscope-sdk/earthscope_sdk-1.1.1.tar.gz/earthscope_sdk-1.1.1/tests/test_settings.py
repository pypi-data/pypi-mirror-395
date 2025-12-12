import json
from pathlib import Path
from textwrap import dedent

import pytest
from pydantic import ValidationError
from pytest import MonkeyPatch

from earthscope_sdk import __version__
from earthscope_sdk.config._compat import _get_legacy_auth_state_path
from earthscope_sdk.config.error import ProfileDoesNotExistError
from earthscope_sdk.config.models import (
    AuthFlowSettings,
    HttpRetrySettings,
    HttpSettings,
    Tokens,
)
from earthscope_sdk.config.settings import (
    _BOOTSTRAP_ENV_VAR,
    SdkSettings,
    _get_config_toml_path,
)

_bootstrap_state_json = json.dumps(
    {
        "oauth2": {
            "audience": "https://bootstrap-audience.earthscope.org",
            "client_id": "bootstrap-client-id",
            "domain": "https://bootstrap-domain.earthscope.org",
            "scope": "bootstrap-scope",
            "access_token": "bootstrap-at",
            "refresh_token": "bootstrap-rt",
            "id_token": "bootstrap-it",
        }
    }
)


@pytest.fixture
def config_toml():
    return _get_config_toml_path()


@pytest.fixture
def legacy_tokens_json():
    return _get_legacy_auth_state_path()


@pytest.fixture(scope="session")
def default_settings():
    return SdkSettings()


class TestSdkSettings:
    def test_defaults(self):
        s = SdkSettings()
        assert s.profile_name == "default"
        assert s.oauth2.audience == "https://api.earthscope.org"
        assert str(s.oauth2.domain) == "https://login.earthscope.org/"
        assert s.oauth2.client_id == "b9DtAFBd6QvMg761vI3YhYquNZbJX5G0"
        assert s.oauth2.scope == "offline_access"
        assert str(s.resources.api_url) == "https://api.earthscope.org/"
        assert s.http.user_agent == f"earthscope-sdk py/{__version__}"
        assert s.http.max_connections is None
        assert s.http.max_keepalive_connections is None
        assert s.http.keepalive_expiry.total_seconds() == 5.0
        assert s.http.timeout_read.total_seconds() == 5.0
        assert s.http.retry.attempts == 3
        assert s.http.retry.timeout.total_seconds() == 20.0
        assert s.http.retry.wait_initial.total_seconds() == 0.1
        assert s.http.retry.wait_max.total_seconds() == 5.0
        assert s.http.retry.wait_jitter.total_seconds() == 1.0
        assert s.http.retry.wait_exp_base == 2
        assert s.oauth2.client_secret is None
        assert s.oauth2.access_token is None
        assert s.oauth2.refresh_token is None
        assert s.oauth2.retry.attempts == 5
        assert s.oauth2.retry.timeout.total_seconds() == 30.0
        assert s.oauth2.retry.wait_initial.total_seconds() == 1.0
        assert s.oauth2.retry.wait_max.total_seconds() == 5.0
        assert s.oauth2.retry.wait_jitter.total_seconds() == 3.0
        assert s.oauth2.retry.wait_exp_base == 2

    def test_profile_does_not_exist_init(self):
        with pytest.raises(ProfileDoesNotExistError):
            SdkSettings(profile_name="foo")

    def test_profile_does_not_exist_env(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv("ES_PROFILE", "foo")
        with pytest.raises(ProfileDoesNotExistError):
            SdkSettings()

    def test_nested_init_with_dict(self):
        s = SdkSettings(oauth2={"scope": "dict-scope"})
        assert s.oauth2.scope == "dict-scope"

    def test_secret_serialization(self):
        s = SdkSettings(
            oauth2={
                "access_token": "foo-at",
                "id_token": "foo-it",
                "refresh_token": "foo-rt",
                "client_secret": "foo-secret",
            }
        )

        dumped = s.model_dump(mode="json")
        assert dumped["oauth2"]["access_token"] == "**********"
        assert dumped["oauth2"]["id_token"] == "**********"
        assert dumped["oauth2"]["refresh_token"] == "**********"
        assert dumped["oauth2"]["client_secret"] == "**********"

        dumped_plaintext = s.model_dump(mode="json", context="plaintext")
        assert dumped_plaintext["oauth2"]["access_token"] == "foo-at"
        assert dumped_plaintext["oauth2"]["id_token"] == "foo-it"
        assert dumped_plaintext["oauth2"]["refresh_token"] == "foo-rt"
        assert dumped_plaintext["oauth2"]["client_secret"] == "foo-secret"


class TestSdkSettingsPrecedence:
    def test_precedence_all(self, config_toml: Path, monkeypatch: MonkeyPatch):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.scope = "default-scope"

                [profile.default]
                oauth2.scope = "profile-scope"
            """)
        )
        monkeypatch.setenv("ES_OAUTH2__SCOPE", "env-scope")
        s = SdkSettings(oauth2=AuthFlowSettings(scope="init-scope"))

        assert s.oauth2.scope == "init-scope"

    def test_precedence_env(self, config_toml: Path, monkeypatch: MonkeyPatch):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.scope = "default-scope"

                [profile.default]
                oauth2.scope = "profile-scope"
            """)
        )
        monkeypatch.setenv("ES_OAUTH2__SCOPE", "env-scope")
        s = SdkSettings()

        assert s.oauth2.scope == "env-scope"

    def test_precedence_profile(self, config_toml: Path, monkeypatch: MonkeyPatch):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.scope = "default-scope"

                [profile.default]
                oauth2.scope = "profile-scope"
            """)
        )
        s = SdkSettings()

        assert s.oauth2.scope == "profile-scope"

    def test_precedence_defaults(self, config_toml: Path, monkeypatch: MonkeyPatch):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.scope = "default-scope"
            """)
        )
        s = SdkSettings()

        assert s.oauth2.scope == "default-scope"

    def test_precedence_bootstrap_state(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)

        s = SdkSettings()
        assert s.oauth2.audience == "https://bootstrap-audience.earthscope.org"
        assert s.oauth2.client_id == "bootstrap-client-id"
        assert str(s.oauth2.domain) == "https://bootstrap-domain.earthscope.org/"
        assert s.oauth2.scope == "bootstrap-scope"
        assert s.oauth2.access_token.get_secret_value() == "bootstrap-at"
        assert s.oauth2.refresh_token.get_secret_value() == "bootstrap-rt"
        assert s.oauth2.id_token.get_secret_value() == "bootstrap-it"


class TestSdkSettingsProfiles:
    def test_profile_settings(self, config_toml: Path):
        config_toml.write_text(
            dedent("""
                [profile.pytest]
                oauth2.scope = "pytest-scope"
            """)
        )
        s = SdkSettings(profile_name="pytest")

        assert s.oauth2.scope == "pytest-scope"

    def test_profile_merging(self, config_toml: Path, monkeypatch: MonkeyPatch):
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.scope = "default-scope"
                oauth2.audience = "default-audience"
                oauth2.client_id = "default-client-id"
                oauth2.domain = "http://default-domain"

                [profile.pytest]
                # intentionally omitting `oauth2.scope` to test merging
                oauth2.audience = "profile-audience"
                oauth2.client_id = "profile-client-id"
                oauth2.domain = "http://profile-domain"
            """)
        )

        # intentionally omitting scope and audience to test merging
        monkeypatch.setenv("ES_OAUTH2__CLIENT_ID", "env-client-id")
        monkeypatch.setenv("ES_OAUTH2__DOMAIN", "http://env-domain")

        # intentionally omitting scope, audience and domain to test merging
        s = SdkSettings(
            profile_name="pytest",
            oauth2=AuthFlowSettings(domain="http://init-domain"),
        )

        assert str(s.resources.api_url) == "https://api.earthscope.org/"
        assert s.oauth2.scope == "default-scope"
        assert s.oauth2.audience == "profile-audience"
        assert s.oauth2.client_id == "env-client-id"
        assert str(s.oauth2.domain) == "http://init-domain/"

    def test_multiple_profiles(self, config_toml: Path):
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.scope = "default-scope"
                oauth2.audience = "default-audience"
                oauth2.client_id = "default-client-id"
                oauth2.domain = "http://default-domain"

                [profile.foo]
                oauth2.scope = "foo-scope"

                [profile.bar]
                oauth2.scope = "bar-scope"
            """)
        )
        foo = SdkSettings(profile_name="foo")
        bar = SdkSettings(profile_name="bar")

        assert foo.oauth2.scope == "foo-scope"
        assert bar.oauth2.scope == "bar-scope"

    def test_legacy_state(self, legacy_tokens_json: Path):
        legacy_tokens_json.write_text(
            dedent("""
                {
                    "audience": "legacy-aud",
                    "domain": "https://legacy-domain.earthscope.org/",
                    "client_id": "legacy-client-id",
                    "scope": "legacy-scope",
                    "api_url": "https://legacy-api.earthscope.org/",
                    "user_agent": "legacy",
                    "refresh_token": "legacy-rt",
                    "access_token": "legacy-at"
                }
            """)
        )

        s = SdkSettings()

        assert s.oauth2.refresh_token.get_secret_value() == "legacy-rt"
        assert s.oauth2.access_token.get_secret_value() == "legacy-at"

        # other keys are not taken
        assert s.oauth2.scope == "offline_access"
        assert s.oauth2.audience == "https://api.earthscope.org"
        assert str(s.oauth2.domain) == "https://login.earthscope.org/"
        assert s.oauth2.client_id == "b9DtAFBd6QvMg761vI3YhYquNZbJX5G0"
        assert s.oauth2.scope == "offline_access"
        assert str(s.resources.api_url) == "https://api.earthscope.org/"
        assert s.http.user_agent == f"earthscope-sdk py/{__version__}"
        assert s.http.max_connections is None
        assert s.http.max_keepalive_connections is None
        assert s.http.keepalive_expiry.total_seconds() == 5.0
        assert s.http.timeout_read.total_seconds() == 5.0
        assert s.oauth2.client_secret is None

    def test_nested_settings_precedence(
        self, config_toml: Path, monkeypatch: MonkeyPatch
    ):
        config_toml.write_text(
            dedent("""
                [default]
                http.max_connections = 11
                http.max_keepalive_connections = 11
                http.timeout_read = 11.1
                http.keepalive_expiry = 11.1
                   
                http.retry.attempts = 11
                http.retry.timeout = 11.1
                http.retry.wait_jitter = 11.1
                http.retry.wait_initial = 11.1

                [profile.pytest]
                http.max_connections = 22
                http.max_keepalive_connections = 22
                http.keepalive_expiry = 22.2
                http.retry.timeout = 22.2
                http.retry.wait_jitter = 22.2
                http.retry.wait_initial = 22.2
            """)
        )

        monkeypatch.setenv("ES_HTTP__MAX_CONNECTIONS", "33")
        monkeypatch.setenv("ES_HTTP__KEEPALIVE_EXPIRY", "33.3")
        monkeypatch.setenv("ES_HTTP__RETRY__WAIT_JITTER", "33.3")
        monkeypatch.setenv("ES_HTTP__RETRY__WAIT_INITIAL", "33.3")

        s = SdkSettings(
            profile_name="pytest",
            http=HttpSettings(
                keepalive_expiry=44.4,
                retry=HttpRetrySettings(wait_initial=44.4),
            ),
        )

        assert s.http.keepalive_expiry.total_seconds() == 44.4
        assert s.http.max_connections == 33
        assert s.http.max_keepalive_connections == 22
        assert s.http.timeout_read.total_seconds() == 11.1

        assert s.http.retry.attempts == 11
        assert s.http.retry.timeout.total_seconds() == 22.2
        assert s.http.retry.wait_jitter.total_seconds() == 33.3
        assert s.http.retry.wait_initial.total_seconds() == 44.4


class TestTokens:
    def test_defaults(self):
        t = Tokens(access_token="at")
        assert t.refresh_token is None
        assert t.id_token is None

        t2 = Tokens(refresh_token="rt")
        assert t2.access_token is None

    def test_one_of_access_or_refresh(self):
        assert Tokens(access_token="at").access_token.get_secret_value() == "at"
        assert Tokens(refresh_token="rt").refresh_token.get_secret_value() == "rt"

        with pytest.raises(ValidationError):
            Tokens(id_token="it")

    def test_access_token_bad_body(self):
        with pytest.raises(ValueError):
            Tokens(access_token="at").access_token_body

    def test_access_token_body(self):
        # expired access token
        at = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im80WDNMM1p0QkN6MmZ5RktMVW9mWiJ9.eyJpc3MiOiJodHRwczovL2xvZ2luLmVhcnRoc2NvcGUub3JnLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTE4NDAzNTA2MTU0OTQyODQyNTgzIiwiYXVkIjoiaHR0cHM6Ly9hcGkuZWFydGhzY29wZS5vcmciLCJpYXQiOjE3MzQ1Nzg5MzQsImV4cCI6MTczNDY2NTMzNCwic2NvcGUiOiJvZmZsaW5lX2FjY2VzcyIsImF6cCI6ImI5RHRBRkJkNlF2TWc3NjF2STNZaFlxdU5aYkpYNUcwIn0.Sz9v95Iru62STcDfZYDXYiqW2zqVsAQ9_XpSaGgWbcXbJzQApG1pPQKL0s7yBw08diepEhUG4dOijdUKugw616kp7TkpH8hniYv7yPwwwdeqZYGTCJ0gfDIzxRYzPXoY1gqPM1WzA-ZPBNOdJyi_LNGS0_jjx4MGJ5NRkL76Us0zP-C9z_IdYA1jRgPrVkOt5AXSwFHNn-4FNDYwL2NE_eO2xfJZm4fHbhSmtWCT7wKJvt4g-viMprOiKK0glf9u2eDxXCP1QFIoNSug1C_esJAe1AbyaRlk0C3y8Zz42K8jMFurCIjI_PenQ4GAH0eunCSwrMPioIZq8k3a4MoKVw"
        t = Tokens(access_token=at)

        t.access_token_body.audience == "https://api.earthscope.org"
        t.access_token_body.client_id == "b9DtAFBd6QvMg761vI3YhYquNZbJX5G0"
        t.access_token_body.issuer == "https://login.earthscope.org/"
        t.access_token_body.subject == "google-oauth2|118403506154942842583"
        t.access_token_body.scope == "offline_access"
        t.access_token_body.grant_type is None

    def test_tokens_loading(self, default_settings: SdkSettings):
        exp = Tokens(access_token="at", id_token="it", refresh_token="rt")
        default_settings.write_tokens(exp)

        # load new settings as if
        actual = SdkSettings()
        assert (
            actual.oauth2.access_token.get_secret_value()
            == exp.access_token.get_secret_value()
        )
        assert (
            actual.oauth2.id_token.get_secret_value() == exp.id_token.get_secret_value()
        )
        assert (
            actual.oauth2.refresh_token.get_secret_value()
            == exp.refresh_token.get_secret_value()
        )


class TestTokensPrecedence:
    def test_tokens_precedence_all(
        self,
        config_toml: Path,
        default_settings: SdkSettings,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)
        default_settings.write_tokens(Tokens(access_token="state-at"))
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.access_token = "default-at"

                [profile.default]
                oauth2.access_token = "profile-at"
            """)
        )
        monkeypatch.setenv("ES_OAUTH2__ACCESS_TOKEN", "env-at")

        t = SdkSettings(oauth2=AuthFlowSettings(access_token="init-at"))
        assert t.oauth2.access_token.get_secret_value() == "init-at"

    def test_tokens_precedence_env(
        self,
        config_toml: Path,
        default_settings: SdkSettings,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)
        default_settings.write_tokens(Tokens(access_token="state-at"))
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.access_token = "default-at"

                [profile.default]
                oauth2.access_token = "profile-at"
            """)
        )
        monkeypatch.setenv("ES_OAUTH2__ACCESS_TOKEN", "env-at")

        t = SdkSettings()
        assert t.oauth2.access_token.get_secret_value() == "env-at"

    def test_tokens_precedence_profile(
        self,
        config_toml: Path,
        default_settings: SdkSettings,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)
        default_settings.write_tokens(Tokens(access_token="state-at"))
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.access_token = "default-at"

                [profile.default]
                oauth2.access_token = "profile-at"
            """)
        )

        t = SdkSettings()
        assert t.oauth2.access_token.get_secret_value() == "profile-at"

    def test_tokens_precedence_defaults(
        self,
        config_toml: Path,
        default_settings: SdkSettings,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)
        default_settings.write_tokens(Tokens(access_token="state-at"))
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.access_token = "default-at"
            """)
        )

        t = SdkSettings()
        assert t.oauth2.access_token.get_secret_value() == "default-at"

    def test_tokens_precedence_state(
        self,
        default_settings: SdkSettings,
        monkeypatch: MonkeyPatch,
    ):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)
        default_settings.write_tokens(Tokens(access_token="state-at"))

        t = SdkSettings()
        assert t.oauth2.access_token.get_secret_value() == "state-at"

    def test_tokens_precedence_legacy(
        self,
        config_toml: Path,
        legacy_tokens_json: Path,
        monkeypatch: MonkeyPatch,
    ):
        legacy_tokens_json.write_text(
            dedent("""
                {
                    "refresh_token": "legacy-rt",
                    "access_token": "legacy-at"
                }
            """)
        )

        # init > legacy
        s = SdkSettings(oauth2=AuthFlowSettings(access_token="init-at"))
        assert s.oauth2.refresh_token.get_secret_value() == "legacy-rt"
        assert s.oauth2.access_token.get_secret_value() == "init-at"

        # env > legacy
        with monkeypatch.context() as m:
            m.setenv("ES_OAUTH2__ACCESS_TOKEN", "env-at")

            s = SdkSettings()
            assert s.oauth2.refresh_token.get_secret_value() == "legacy-rt"
            assert s.oauth2.access_token.get_secret_value() == "env-at"

        # config.toml profile > default > legacy
        config_toml.write_text(
            dedent("""
                [default]
                oauth2.refresh_token = "default-rt"
                oauth2.access_token = "default-at"

                [profile.default]
                oauth2.access_token = "profile-at"
            """)
        )

        s = SdkSettings()
        assert s.oauth2.refresh_token.get_secret_value() == "default-rt"
        assert s.oauth2.access_token.get_secret_value() == "profile-at"
        config_toml.unlink()

        # legacy > bootstrap
        with monkeypatch.context() as m:
            m.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)

            s = SdkSettings()
            assert s.oauth2.refresh_token.get_secret_value() == "legacy-rt"
            assert s.oauth2.access_token.get_secret_value() == "legacy-at"
            assert s.oauth2.scope == "bootstrap-scope"


class TestBootstrapSettings:
    def test_bootstrap_settings(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, _bootstrap_state_json)

        s = SdkSettings()
        assert s.oauth2.audience == "https://bootstrap-audience.earthscope.org"
        assert s.oauth2.client_id == "bootstrap-client-id"
        assert str(s.oauth2.domain) == "https://bootstrap-domain.earthscope.org/"
        assert s.oauth2.scope == "bootstrap-scope"
        assert s.oauth2.access_token.get_secret_value() == "bootstrap-at"
        assert s.oauth2.refresh_token.get_secret_value() == "bootstrap-rt"
        assert s.oauth2.id_token.get_secret_value() == "bootstrap-it"

    def test_bootstrap_settings_invalid_json(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, "invalid-json")

        s = SdkSettings()
        assert s.oauth2.audience == "https://api.earthscope.org"
        assert s.oauth2.client_id == "b9DtAFBd6QvMg761vI3YhYquNZbJX5G0"
        assert str(s.oauth2.domain) == "https://login.earthscope.org/"
        assert s.oauth2.scope == "offline_access"
        assert s.oauth2.access_token is None
        assert s.oauth2.refresh_token is None
        assert s.oauth2.id_token is None

    def test_bootstrap_settings_empty_json(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv(_BOOTSTRAP_ENV_VAR, "{}")

        s = SdkSettings()
        assert s.oauth2.audience == "https://api.earthscope.org"
        assert s.oauth2.client_id == "b9DtAFBd6QvMg761vI3YhYquNZbJX5G0"
        assert str(s.oauth2.domain) == "https://login.earthscope.org/"
        assert s.oauth2.scope == "offline_access"
        assert s.oauth2.access_token is None
        assert s.oauth2.refresh_token is None
        assert s.oauth2.id_token is None

    def test_bootstrap_settings_other_keys(self, monkeypatch: MonkeyPatch):
        monkeypatch.setenv(
            _BOOTSTRAP_ENV_VAR,
            json.dumps(
                {
                    "http": {
                        "timeout_read": 10.0,
                        "user_agent": "bootstrap-ua",
                    },
                    "oauth2": {
                        "scope": "bootstrap-scope",
                    },
                }
            ),
        )

        s = SdkSettings()
        # bootstrap settings
        assert s.http.timeout_read.total_seconds() == 10.0
        assert s.http.user_agent == "bootstrap-ua"
        assert s.oauth2.scope == "bootstrap-scope"

        # defaults
        assert s.http.timeout_connect.total_seconds() == 5.0
        assert s.oauth2.audience == "https://api.earthscope.org"
        assert s.oauth2.client_id == "b9DtAFBd6QvMg761vI3YhYquNZbJX5G0"
        assert str(s.oauth2.domain) == "https://login.earthscope.org/"
        assert s.oauth2.access_token is None
        assert s.oauth2.refresh_token is None
        assert s.oauth2.id_token is None


class TestAuthFlowSettings:
    @pytest.mark.parametrize(
        "host,allowed",
        [
            ("earthscope.org", True),
            ("api.earthscope.org", True),
            ("data.earthscope.org", True),
            ("foo.earthscope.org", True),
            ("foo.subdomain.earthscope.org", True),
            ("earthscope.foo.org", False),
            ("example.com", False),
            ("foo.example.com", False),
            ("earthscope.example.com", False),
            ("foo.earthscope.example.com", False),
        ],
    )
    def test_allowed_hosts_defaults(self, host: str, allowed: bool):
        s = AuthFlowSettings()
        assert s.is_host_allowed(host) == allowed

    def test_allowed_hosts_cache(self):
        s = AuthFlowSettings()
        assert "foo.earthscope.org" not in s.allowed_hosts
        assert s.is_host_allowed("foo.earthscope.org")
        assert "foo.earthscope.org" in s.allowed_hosts
