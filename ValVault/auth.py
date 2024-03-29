from dataclasses import asdict
from json import JSONDecodeError
from time import time
from typing import Optional

from dataclasses_json import DataClassJsonMixin

from ValLib import Auth, AuthException, User, authenticate, cookie_token

from .debug import Level, log


class EntryAuth(Auth, DataClassJsonMixin):
    @classmethod
    def _trans(cls, auth: Auth):
        return cls.from_dict(asdict(auth)).to_json()

    @classmethod
    def _reverse(cls, raw: str):
        try:
            auth = EntryAuth.from_json(raw)
        except JSONDecodeError:
            auth = None
        return auth


ONE_DAY = 86400.0


def has_expired(auth: Auth):
    return time() > auth.expire


def cookies_expired(auth: Auth):
    return (time() - auth.created) > ONE_DAY * 30


def try_cookies(auth: Auth) -> Optional[Auth]:
    try:
        token, cookies = cookie_token(auth.cookies)
        auth.token = token
        auth.cookies = cookies
        auth.created = time()
        return auth
    except AuthException:
        return None


def best_auth(user: User, auth: Auth, remember: bool):
    if auth.remember and not cookies_expired(auth):
        new_auth = try_cookies(auth)
        if new_auth is not None:
            return new_auth

    log(Level.DEBUG, f"Expired cookies for {user.username}")
    return authenticate(user, remember)


def get_auth(user: User, auth: Optional[Auth], remember=False, reauth=False):
    if auth is None:
        log(Level.DEBUG, f"Auth {user.username} for the first time")
        return authenticate(user, remember)

    if reauth or has_expired(auth):
        log(Level.DEBUG, (f"ReAuth for " if reauth else "Expired Auth for ") + user.username)
        return best_auth(user, auth, remember)

    log(Level.DEBUG, f"Auth cache hit for {user.username}")
    return auth
