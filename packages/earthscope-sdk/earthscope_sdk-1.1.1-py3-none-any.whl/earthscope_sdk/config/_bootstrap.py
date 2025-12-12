"""
This module facilitates bootstrapping SDK settings from a JSON-encoded environment variable.
"""

import json
import logging
import os

from pydantic_settings import PydanticBaseSettingsSource

logger = logging.getLogger(__name__)


class BootstrapEnvironmentSettingsSource(PydanticBaseSettingsSource):
    """
    This SettingsSource facilitates bootstrapping the SDK from a special environment variable.

    The environment variable should be a JSON string of the expected SDK settings and structure.
    """

    def __init__(self, settings_cls, env_var: str):
        super().__init__(settings_cls)
        self._env_var = env_var

    def __call__(self):
        try:
            bootstrap_settings = os.environ[self._env_var]
        except KeyError:
            return {}

        try:
            return json.loads(bootstrap_settings)
        except json.JSONDecodeError:
            logger.warning(
                f"Found bootstrap environment variable '{self._env_var}', but unable to decode content as JSON"
            )
            return {}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(env_var='{self._env_var}')"

    def get_field_value(self, *args, **kwargs): ...  # unused abstract method
