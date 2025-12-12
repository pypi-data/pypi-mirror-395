from contextlib import suppress
from functools import cached_property
from typing import Annotated, Any, Type

from pydantic import Field, TypeAdapter, ValidationError, field_validator
from pydantic_settings import (
    BaseSettings,
    InitSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from earthscope_sdk.config._bootstrap import BootstrapEnvironmentSettingsSource
from earthscope_sdk.config._compat import LegacyEarthScopeCLISettingsSource
from earthscope_sdk.config._util import deep_merge, get_config_dir, slugify
from earthscope_sdk.config.error import ProfileDoesNotExistError
from earthscope_sdk.config.models import SdkBaseSettings, Tokens

_BOOTSTRAP_ENV_VAR = "ES_BOOTSTRAP_SETTINGS"
"""Environment variable for bootstrapping the SDK"""

_DEFAULT_PROFILE = "default"
"""Default profile name"""

_LOCAL_APP_DIR = get_config_dir(app_name="earthscope")
"""Local SDK application directory"""


def _get_config_toml_path():
    """
    Local SDK configuration file
    """
    return _LOCAL_APP_DIR / "config.toml"


def _get_profile_dir(profile_name: str):
    """
    Retrieve the local SDK directory for the named profile
    """
    return _LOCAL_APP_DIR / slugify(profile_name)


def _get_profile_tokens_file(profile_name: str):
    """
    Retrieve the local SDK tokens file for the named profile
    """
    profile_dir = _get_profile_dir(profile_name)
    return profile_dir / "tokens.json"


class _SdkGlobalSettings(BaseSettings):
    """
    EarthScope SDK global settings; not for direct use.

    This class only loads settings from config.toml.
    """

    defaults: Annotated[
        SdkBaseSettings,
        Field(validation_alias="default"),
    ] = {}

    profile_settings_by_name: Annotated[
        dict[str, SdkBaseSettings],
        Field(validation_alias="profile"),
    ] = {}

    model_config = SettingsConfigDict(
        extra="ignore",
        frozen=True,
        nested_model_default_partial_update=True,
        populate_by_name=True,
    )

    def get_merged(self, profile_name: str):
        """
        Get profile-specific settings merged with defaults
        """
        try:
            p = self.profile_settings_by_name[profile_name]
        except KeyError:
            raise ProfileDoesNotExistError(f"Profile '{profile_name}' does not exist")

        defaults = self.defaults.model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude_defaults=True,
        )
        profile_specific = p.model_dump(
            exclude_defaults=True,  # defer to top-level field defaults
            exclude_unset=True,  # only keep explicitly set fields
            exclude_none=True,
        )

        # order is imporant; profile-specific args override default args
        return deep_merge(defaults, profile_specific, profile_name=profile_name)

    @field_validator("profile_settings_by_name", mode="before")
    @classmethod
    def ensure_default_profile(cls, v: dict[str, dict]):
        """
        Ensure the default profile exists
        """
        v.setdefault(_DEFAULT_PROFILE, {})
        return v

    @classmethod
    def settings_customise_sources(cls, settings_cls: Type[BaseSettings], **_):
        """
        Override the loading chain to exclusively check ~/.earthscope/config.toml
        """
        # we get the file path dynamically to allow monkeypatching for tests
        toml_path = _get_config_toml_path()
        toml_settings = TomlConfigSettingsSource(settings_cls, toml_path)

        return (toml_settings,)


class _GlobalSettingsSource(PydanticBaseSettingsSource):
    """
    This SettingsSource facilitates falling back to settings configured in config.toml
    and state in tokens.json when loading the configuration chain in SdkSettings.

    Consolidates merged profile state with state loaded from a profile's tokens.json file
    """

    def __init__(self, settings_cls, *keys: str):
        super().__init__(settings_cls)
        self._keys = keys

    def __call__(self):
        # Extract profile
        profile_name = _DEFAULT_PROFILE
        for k in self._keys:
            with suppress(KeyError):
                profile_name = self._current_state[k]
                break

        # Load global merged settings
        merged = _SdkGlobalSettings().get_merged(profile_name)

        # Load from tokens.json
        tokens_json = {}
        with suppress(FileNotFoundError, ValidationError):
            raw = _get_profile_tokens_file(profile_name).read_bytes()
            tokens = Tokens.model_validate_json(raw)
            tokens_json = tokens.model_dump(
                exclude_none=True,
                exclude_unset=True,
                exclude_defaults=True,
            )

        # order is imporant; init args override tokens.json args
        return deep_merge({"oauth2": tokens_json}, merged)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def get_field_value(self, *args, **kwargs): ...  # unused abstract method


class _InitSettingsWithoutDefaultSource(InitSettingsSource):
    """
    InitSettingsSource behavior but excludes default values & unset fields
    to allow values from lower-precedence settings sources to bubble up.
    """

    def __init__(self, other: InitSettingsSource):
        super().__init__(
            other.settings_cls,
            other.init_kwargs,
            other.nested_model_default_partial_update,
        )
        self.dict_adapter = TypeAdapter(dict[str, Any])

    def __call__(self) -> dict[str, Any]:
        return self.dict_adapter.dump_python(
            self.init_kwargs,
            exclude_defaults=True,
            exclude_unset=True,
        )


class SdkSettings(SdkBaseSettings, BaseSettings):
    """
    EarthScope SDK settings.

    Use `profile_name` to utilize a named profile from `~/.earthscope/config.toml`

    Settings loading chain (order of precedence):
    1. arguments passed to constructor
    2. environment variables
    3. dotenv variables
    4. ~/.earthscope/config.toml
    """

    profile_name: Annotated[
        str,
        Field(validation_alias="es_profile"),
        # NOTE: aliases do not include the env_prefix by default; add it explicitly
    ]

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_prefix="ES_",
        extra="ignore",
        frozen=True,
        nested_model_default_partial_update=True,
        populate_by_name=True,
    )

    @cached_property
    def profile_dir(self):
        """
        The path to the local SDK directory for the named profile
        """
        return _get_profile_dir(self.profile_name)

    @cached_property
    def tokens_file(self):
        """
        The path to the tokens file for the named profile
        """
        return _get_profile_tokens_file(self.profile_name)

    def delete_tokens(self, missing_ok=False):
        """
        Delete tokens from this named profile's state

        Args:
            missing_ok: Whether or not to throw an error if the file does not exist

        Returns:
            this auth flow
        """
        self.tokens_file.unlink(missing_ok=missing_ok)
        return self

    def write_tokens(self, tokens: Tokens):
        """
        Write tokens to this named profile's state

        Args:
            tokens: the tokens to persist in local storage
        """
        body = tokens.model_dump_json(
            include=Tokens.model_fields.keys(),
            indent=2,
            context="plaintext",  # write SecretStr's actual values in plaintext
            exclude_none=True,
        )
        self.tokens_file.parent.mkdir(parents=True, exist_ok=True)
        self.tokens_file.write_text(body)

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: InitSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        **_,
    ):
        """
        Override the loading chain to additionally check ~/.earthscope/config.toml
        """

        # Init settings, but without defaults & unset values
        init_settings = _InitSettingsWithoutDefaultSource(init_settings)

        # Check for all the ways profile name may be supplied
        alias = SdkSettings.model_fields["profile_name"].validation_alias
        global_settings = _GlobalSettingsSource(settings_cls, "profile_name", alias)

        # Check for bootstrapping configuration
        bootstrap_settings = BootstrapEnvironmentSettingsSource(
            settings_cls,
            _BOOTSTRAP_ENV_VAR,
        )

        # Compatibility with earthscope-cli v0.x.x state:
        # If we find this file, we only care about the access and refresh tokens
        keep_keys = {"access_token", "refresh_token"}
        legacy_settings = LegacyEarthScopeCLISettingsSource(settings_cls, *keep_keys)

        # Order of precedence
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            global_settings,
            legacy_settings,
            bootstrap_settings,
        )
