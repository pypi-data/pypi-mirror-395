"""
This module facilitates compatibility with EarthScope CLI v0.x.x
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Union

from pydantic_settings import PydanticBaseSettingsSource

logger = logging.getLogger(__name__)

####
# The following code is nearly verbatim from Click's source (which is what Typer uses underneath)
# https://github.com/pallets/click/blob/main/src/click/utils.py.
#
# The various functions and consts have been renamed to be "private"
#
# Click's get_app_dir() was used to determine the "application directory" in earthscope-cli v0.x.x.
# whereas this has moved to ~/.earthscope/ starting in 1.0.0
#
# We replicate this functionality here so that the SDK does not need a dependency on Click.
####

_WIN = sys.platform.startswith("win")


def _posixify(name: str) -> str:
    return "-".join(name.split()).lower()


def _get_legacy_app_dir(
    app_name: str,
    roaming: bool = True,
    force_posix: bool = False,
) -> str:
    r"""Returns the config folder for the application.  The default behavior
    is to return whatever is most appropriate for the operating system.

    To give you an idea, for an app called ``"Foo Bar"``, something like
    the following folders could be returned:

    Mac OS X:
      ``~/Library/Application Support/Foo Bar``
    Mac OS X (POSIX):
      ``~/.foo-bar``
    Unix:
      ``~/.config/foo-bar``
    Unix (POSIX):
      ``~/.foo-bar``
    Windows (roaming):
      ``C:\Users\<user>\AppData\Roaming\Foo Bar``
    Windows (not roaming):
      ``C:\Users\<user>\AppData\Local\Foo Bar``

    .. versionadded:: 2.0

    :param app_name: the application name.  This should be properly capitalized
                     and can contain whitespace.
    :param roaming: controls if the folder should be roaming or not on Windows.
                    Has no effect otherwise.
    :param force_posix: if this is set to `True` then on any POSIX system the
                        folder will be stored in the home folder with a leading
                        dot instead of the XDG config home or darwin's
                        application support folder.
    """
    if _WIN:
        key = "APPDATA" if roaming else "LOCALAPPDATA"
        folder = os.environ.get(key)
        if folder is None:
            folder = os.path.expanduser("~")
        return os.path.join(folder, app_name)
    if force_posix:
        return os.path.join(os.path.expanduser(f"~/.{_posixify(app_name)}"))
    if sys.platform == "darwin":
        return os.path.join(
            os.path.expanduser("~/Library/Application Support"), app_name
        )
    return os.path.join(
        os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config")),
        _posixify(app_name),
    )


####
# end of Click code
####

# Legacy state was just the exact response body from Auth0 e.g.
# {
#   "access_token": "<TOKEN>",
#   "id_token": "<TOKEN>",
#   "refresh_token": "<TOKEN>",
#   "scope": "openid profile email offline_access",
#   "expires_at": 1734742981,
#   "issued_at": 1734714181
# }

# the following is how the local app directory was determined in v0.x.x
_LEGACY_APP_DIR = Path(
    os.environ.get("APP_DIRECTORY", _get_legacy_app_dir("earthscope-cli"))
)


def _get_legacy_auth_state_path():
    return _LEGACY_APP_DIR / "sso_tokens.json"


class LegacyEarthScopeCLISettingsSource(PydanticBaseSettingsSource):
    """
    This SettingsSource facilitates migrating earthscope-cli v0.x.x local state into
    earthscope-sdk v1.x.x state
    """

    def __init__(self, settings_cls, *keys: str):
        super().__init__(settings_cls)
        self._keys = keys

    def __call__(self):
        # load path dynamically so we can override in tests
        state_path = _get_legacy_auth_state_path()

        # attempt to load from legacy sso_tokens.json
        try:
            with state_path.open() as f:
                state: dict[str, Union[str, int]] = json.load(f)

        # In either error case, just return an empty
        except json.JSONDecodeError:
            logger.warning(
                f"Found legacy earthscope-cli state at '{state_path}', but unable to decode content as JSON"
            )
            return {}

        except FileNotFoundError:
            return {}

        # only preserve specific keys if non-null
        settings = {k: v for k in self._keys if (v := state.get(k)) is not None}
        return {"oauth2": settings}

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def get_field_value(self, *args, **kwargs): ...  # unused abstract method
