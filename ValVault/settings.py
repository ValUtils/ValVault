from ValStorage import get_settings as load_settings

from .structs import Settings
from .storage import settingsPath


def get_settings():
    return load_settings(Settings, settingsPath / "config.json")
