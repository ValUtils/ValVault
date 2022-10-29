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
	return ValVault.get_auth(user)

def test_db():
	import ValVault
	from ValVault.storage import json_write, settingsPath
	json_write({"insecure": True},settingsPath / "config.json")
	ValVault.init()
	username = getenv("USERNAME")
	password = getenv("PASSWORD")
	ValVault.new_user(username, password)
	assert username in ValVault.get_users(), "Username not in db"
	assert ValVault.get_pass(username) == password, "Password not in db"
	