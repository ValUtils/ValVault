import platform
import json
from pathlib import Path
from os import getenv

def save_to_drive(data, file):
	f = open(file, "w")
	f.write(data)
	f.close()

def read_from_drive(file):
	f = open(file, "r")
	data = f.read()
	f.close()
	return data

def json_write(data, file):
	jsonData = json.dumps(data,indent=4)
	save_to_drive(jsonData, file)

def json_read(file):
	rawData = read_from_drive(file)
	data = json.loads(rawData)
	return data

def create_path(path: Path):
	if(path.is_dir()):
		return
	path.mkdir()

def set_path():
	global settingsPath
	if (platform.system() == "Windows"):
		appdata = Path(getenv('APPDATA'))
		settingsPath = appdata / "ValVault"
		create_path(settingsPath)
	elif (platform.system() == "Linux"):
		home = Path(getenv('HOME'))
		settingsPath = home / ".ValVault"
		create_path(settingsPath)

set_path()