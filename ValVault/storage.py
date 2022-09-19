import platform
import json
from pathlib import Path
from os import getenv

def saveToDrive(data, file):
	f = open(file, "w")
	f.write(data)
	f.close()

def readFromDrive(file):
	f = open(file, "r")
	data = f.read()
	f.close()
	return data

def jsonWrite(data, file):
	jsonData = json.dumps(data,indent=4)
	saveToDrive(jsonData, file)

def jsonRead(file):
	rawData = readFromDrive(file)
	data = json.loads(rawData)
	return data

def createPath(path: Path):
	if(path.is_dir()):
		return
	path.mkdir()

def setPath():
	global settingsPath
	if (platform.system() == "Windows"):
		appdata = Path(getenv('APPDATA'))
		settingsPath = appdata / "ValVault"
		createPath(settingsPath)
	elif (platform.system() == "Linux"):
		home = Path(getenv('HOME'))
		settingsPath = home / ".ValVault"
		createPath(settingsPath)

setPath()