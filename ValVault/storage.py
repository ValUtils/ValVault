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

def linux_config():
	xdg = getenv("XDG_CONFIG_HOME")
	if (xdg):
		return Path(xdg) / "ValVault"
	home = Path(getenv('HOME'))
	return home / ".ValVault"

def set_path():
	global settingsPath
	if (platform.system() == "Windows"):
		appdata = Path(getenv('APPDATA'))
		settingsPath = appdata / "ValVault"
		create_path(settingsPath)
	elif (platform.system() == "Linux"):
		settingsPath = linux_config()
		create_path(settingsPath)

set_path()