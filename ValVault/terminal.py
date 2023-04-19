from getpass import getpass as inputPass
from ValLib.riot import authenticate, AuthException
from ValLib.structs import User, Auth

from .database import EncryptedDB
from .settings import get_settings

db: EncryptedDB


def re_auth() -> Auth:
    print(f"Wrong username or password, type username and password to retry!")
    username = input("User: ")
    password = inputPass("Password: ")
    db.save_user(username, password)
    return get_auth(User(username, password))


def get_auth(user: User) -> Auth:
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


def set_alias(user, alias):
    return db.set_alias(user, alias)


def get_valid_pass() -> str:
    dbPassword = inputPass("Local password: ")
    if not dbPassword:
        return get_valid_pass()
    return dbPassword


def get_aliases():
    return db.get_aliases()


def get_name(alias):
    return db.get_name(alias)


def set_vault() -> EncryptedDB:
    settings = get_settings()
    if settings.insecure:
        db = EncryptedDB(" ")
        return db
    dbPassword = get_valid_pass()
    db = EncryptedDB(dbPassword)
    return db


def init_vault():
    global db
    try:
        return db
    except NameError:
        db = set_vault()
        return db


__all__ = [
    "get_auth", "get_users", "get_pass",
    "get_aliases", "get_name",
    "new_user", "init_vault",
    "User", "Auth",
]
