from .structs import Settings
from .storage import read_from_drive, save_to_drive, settingsPath

def get_settings() -> Settings:
	settings = read_from_drive(settingsPath / "config.json")
	return Settings().from_json(settings)
