import os

from ..config import DEFAULT_CONFIG_FILES


def find_default_config_file() -> str:
    for filename in DEFAULT_CONFIG_FILES:
        if os.path.exists(os.path.expanduser(filename)):
            return os.path.expanduser(filename)
    return ""
