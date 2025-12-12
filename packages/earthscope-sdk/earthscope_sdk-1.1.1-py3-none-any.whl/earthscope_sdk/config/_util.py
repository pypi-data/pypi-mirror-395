import pathlib
from functools import reduce


def _merge(a: dict, b: dict):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                _merge(a[key], b[key])
                continue

        a[key] = b[key]

    return a


def deep_merge(*mappings: dict, **kwargs):
    """
    Merge all of the dictionaries provided, reursing into nested dictionaries.

    Behavior:
    - The precedence increases from left to right, with keyword arguments as the highest precedence.
    - The leftmost dictionary is modified in-place. Pass an empty dictionary first to avoid modification of inputs.
    """
    return reduce(_merge, (*mappings, kwargs))


def get_config_dir(app_name: str):
    r"""
    Returns the hidden config folder in the user's home directory for the application.

    Mac OS X:
        `~/.app-name`
    Unix:
        `~/.app-name`
    Windows:
        `C:\Users\<user>\.app-name`
    """
    app_slug = slugify(app_name)
    config_dir = pathlib.Path.home() / f".{app_slug}"
    return config_dir


def slugify(name: str) -> str:
    """
    Convert the given name into a slug which can be used more easily in file names
    """
    return "-".join(name.split()).lower()
