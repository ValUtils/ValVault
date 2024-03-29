from getpass import getpass as inputPass

from ValLib.exceptions import AuthException
from ValLib.structs import Auth, ExtraAuth, User

from .database import EncryptedDB, EntryNotFoundException
from .debug import Level, log
from .settings import get_settings

db: EncryptedDB


def re_auth() -> ExtraAuth:
    log(Level.DEBUG, "Getting new user because of auth error")
    print(f"Wrong username or password, type username and password to retry!")
    username = input("User: ")
    password = inputPass("Password: ")
    entry = db.save_user(username, password)
    return get_auth(entry.as_user())


def get_auth(user: User, remember=True, reauth=False) -> ExtraAuth:
    try:
        return db.get_auth(user, remember, reauth)
    except AuthException:
        return re_auth()


def get_users():
    log(Level.FULL, "Get users", "terminal")
    return db.users


def get_pass(username: str):
    log(Level.FULL, "Get pasword", "terminal")
    try:
        return db.find_one(username=username).password
    except EntryNotFoundException:
        return inputPass("Password: ")


def new_user(username: str, password: str):
    log(Level.FULL, f"Saving new user {username}", "terminal")
    return db.save_user(username, password)


def set_alias(username: str, alias: str):
    log(Level.FULL, f"Setting alias for {username} as {alias}", "terminal")
    try:
        entry = db.find_one(username=username)
        entry.alias = alias
        db.db.save()
    except EntryNotFoundException:
        log(Level.INFO, f"User with alias {username} not found", "terminal")


def get_valid_pass() -> str:
    log(Level.FULL, "Getting valid password", "terminal")
    dbPassword = inputPass("Local password: ")
    if not dbPassword:
        return get_valid_pass()
    return dbPassword


def get_aliases():
    log(Level.FULL, "Get aliases", "terminal")
    return db.aliases


def get_name(alias: str):
    log(Level.FULL, f"Get name from alias {alias}", "terminal")
    try:
        return db.find_one(alias=alias).username
    except EntryNotFoundException:
        log(Level.INFO, f"User with alias {alias} not found", "terminal")
        return alias


def set_vault() -> EncryptedDB:
    settings = get_settings()
    if settings.insecure:
        db = EncryptedDB(" ")
        return db
    dbPassword = get_valid_pass()
    db = EncryptedDB(dbPassword)
    return db


def init_vault():
    log(Level.DEBUG, "Initing vault", "terminal")
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
    "User", "ExtraAuth", "Auth",
]
