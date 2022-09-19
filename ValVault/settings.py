from .structs import Settings
from .storage import jsonRead, jsonWrite, settingsPath

def get_settings() -> Settings:
	settings = jsonRead(settingsPath / "config.json")
	return Settings(settings["insecure"])