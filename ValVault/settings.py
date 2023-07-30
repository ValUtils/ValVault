from ValStorage import get_settings as load_settings

from .storage import settingsPath
from .structs import Settings


def get_settings():
    return load_settings(Settings, settingsPath / "config.json")
