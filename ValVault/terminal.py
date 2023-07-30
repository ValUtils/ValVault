from getpass import getpass as inputPass

from ValLib.riot import AuthException
from ValLib.structs import Auth, User

from .database import EncryptedDB
from .debug import Level, log
from .settings import get_settings

db: EncryptedDB


def re_auth() -> Auth:
    log(Level.DEBUG, "Getting new user because of auth error")
    print(f"Wrong username or password, type username and password to retry!")
    username = input("User: ")
    password = inputPass("Password: ")
    db.save_user(username, password)
    return get_auth(User(username, password))


def get_auth(user: User, remember=True, reauth=False) -> Auth:
    try:
        return db.get_auth(user, remember, reauth)
    except AuthException:
        return re_auth()


def get_users():
    log(Level.FULL, "Get users", "terminal")
    return db.get_users()


def get_pass(user):
    log(Level.FULL, "Get pasword", "terminal")
    password = db.get_passwd(user)
    if not password:
        password = inputPass("Password: ")
    return password


def new_user(user, password):
    log(Level.FULL, f"Saving new user {user}", "terminal")
    return db.save_user(user, password)


def set_alias(user, alias):
    log(Level.FULL, f"Setting alias for {user} as {alias}", "terminal")
    return db.set_alias(user, alias)


def get_valid_pass() -> str:
    log(Level.FULL, "Getting valid password", "terminal")
    dbPassword = inputPass("Local password: ")
    if not dbPassword:
        return get_valid_pass()
    return dbPassword


def get_aliases():
    log(Level.FULL, "Get aliases", "terminal")
    return db.get_aliases()


def get_name(alias):
    log(Level.FULL, f"Get name from alias {alias}", "terminal")
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
    "User", "Auth",
]
