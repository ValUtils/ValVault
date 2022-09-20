from os import getenv
def add_path():
	import os.path
	import sys
	path = os.path.realpath(os.path.abspath(__file__))
	sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

add_path()

def test_auth():
	import ValVault
	username = getenv("USERNAME")
	password = getenv("PASSWORD")
	user = ValVault.User(username, password)
	return ValVault.getAuth(user)

def test_db():
	import ValVault
	from ValVault.storage import jsonWrite, settingsPath
	jsonWrite({"insecure": True},settingsPath / "config.json")
	ValVault.init()
	username = getenv("USERNAME")
	password = getenv("PASSWORD")
	ValVault.newUser(username, password)
	assert username in ValVault.getUsers(), "Username not in db"
	assert ValVault.getPass(username) == password, "Password not in db"
	