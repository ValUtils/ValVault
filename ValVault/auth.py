from getpass import getpass as inputPass

from .settings import get_settings
from .exceptions import AuthException
from .structs import User
from .riot import authenticate
from .password import EncryptedDB

db: EncryptedDB

def reAuth():
	print(f"Wrong username or password, type username and password to retry!")
	username = input("User: ")
	password = inputPass("Password: ")
	db.saveUser(username, password)
	return getAuth(User(username, password))

def getAuth(user: User):
	try:
		return authenticate(user)
	except AuthException:
		return reAuth()

def getUsers():
	return db.getUsers()

def getPass(user):
	password = db.getPasswd(user)
	if not password:
		password = inputPass("Password: ")
	return password

def newUser(user, password):
	return db.saveUser(user, password)

def getValidPass():
	dbPassword = inputPass("Local password: ")
	if (not dbPassword):
		return getValidPass()
	return dbPassword

def init():
	global db
	settings = get_settings()
	if (settings.insecure):
		db = EncryptedDB(" ")
		return
	dbPassword = getValidPass()
	db = EncryptedDB(dbPassword)
