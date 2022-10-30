from ValLib.storage import *

def set_path():
	global settingsPath
	utilsPath = utils_path()
	settingsPath = utilsPath / "vault"
	create_path(settingsPath)

set_path()
