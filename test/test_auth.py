from os import getenv
def add_path():
	import os.path
	import sys
	path = os.path.realpath(os.path.abspath(__file__))
	sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

add_path()

def test_add_col():
	import ValVault
	username = getenv("USERNAME")
	password = getenv("PASSWORD")
	user = ValVault.User(username, password)
	return ValVault.getAuth(user)