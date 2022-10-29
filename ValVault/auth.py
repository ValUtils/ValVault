from getpass import getpass as inputPass

from .settings import get_settings
from .exceptions import AuthException
from .structs import User
from .riot import authenticate
from .password import EncryptedDB

db: EncryptedDB = None

def re_auth():
	print(f"Wrong username or password, type username and password to retry!")
	username = input("User: ")
	password = inputPass("Password: ")
	db.save_user(username, password)
	return get_auth(User(username, password))

def get_auth(user: User):
	try:
		return authenticate(user)
	except AuthException:
		return re_auth()

def get_users():
	return db.get_users()

def get_pass(user):
	password = db.get_passwd(user)
	if not password:
		password = inputPass("Password: ")
	return password

def new_user(user, password):
	return db.save_user(user, password)

def get_valid_pass():
	dbPassword = inputPass("Local password: ")
	if (not dbPassword):
		return get_valid_pass()
	return dbPassword

def init():
	global db
	if (db):
		return
	settings = get_settings()
	if (settings.insecure):
		db = EncryptedDB(" ")
		return
	dbPassword = get_valid_pass()
	db = EncryptedDB(dbPassword)
