from .structs import Settings
from .storage import json_read, settingsPath

def get_settings() -> Settings:
	settings = json_read(settingsPath / "config.json")
	return Settings(settings["insecure"])