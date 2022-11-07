from .structs import Settings
from .storage import read_from_drive, save_to_drive, settingsPath

def get_settings() -> Settings:
	try:
		settings = read_from_drive(settingsPath / "config.json")
		return Settings().from_json(settings)
	except:
		pass
	settings = Settings().from_json(r"{}")
	save_to_drive(settings.to_json(), settingsPath / "config.json")
	return settings
