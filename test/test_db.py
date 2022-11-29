from os import getenv
import pytest
import shutil

def add_path():
	import os.path
	import sys
	path = os.path.realpath(os.path.abspath(__file__))
	sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

add_path()

from ValVault import (
	init_vault, new_user,
	get_users, get_pass,
	get_name, get_aliases,
)
from ValVault.storage import json_write, settingsPath
from ValLib.storage import utilsPath

def clean_up():
	import ValVault.auth
	ValVault.auth.db = None
	if (not getenv("VALUTILS_PATH")):
		return
	shutil.rmtree(utilsPath)

@pytest.fixture(scope="function", autouse=True)
def init_env(request):
	settingsPath.mkdir(parents=True, exist_ok=True)
	json_write({"insecure": True}, settingsPath / "config.json")
	init_vault()
	request.addfinalizer(clean_up)

def test_db():
	username = getenv("USERNAME")
	password = getenv("PASSWORD")
	new_user(username, password)
	assert username in get_users(), "Username not in db"
	assert get_pass(username) == password, "Password not in db"

def test_alias():
	from ValVault.auth import db
	username = getenv("USERNAME")
	password = getenv("PASSWORD")
	alias = "alias"
	db.save_user(username, password, alias)
	assert get_name(alias) == username
	assert alias in get_aliases()
