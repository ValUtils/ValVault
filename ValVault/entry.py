from typing import Optional

from pykeepass.entry import Entry as KpEntry

from ValLib.api import get_extra_auth, get_shard
from ValLib.structs import Auth, ExtraAuth, User

from .auth import EntryAuth, get_auth


class EntryException(BaseException):
    """Missing or malformed KpEntry when generating custom Entry"""
    pass


class Entry():
    entry: KpEntry
    _username: str = ""
    _password: str = ""
    _alias: str = ""
    _alt: bool = False
    _auth: Optional[Auth] = None
    _region: Optional[str] = None

    @property
    def alias(self):
        return self._alias

    @alias.setter
    def alias(self, value: str):
        self.set_custom_property("alias", value)
        self._alias = value

    @property
    def alt(self):
        return self._alt

    @alt.setter
    def alt(self, value: bool):
        self.set_custom_property("alt", str(int(value)))
        self._alt = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value: str):
        self.entry.username = value
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value: str):
        self.entry.password = value
        self._password = value

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, value: str):
        self.set_custom_property("region", value)
        self._region = value

    def set_custom_property(self, key, value):
        self.entry.set_custom_property(key, value)

    @property
    def auth(self):
        return self._auth

    @auth.setter
    def auth(self, auth: Auth):
        self._auth = auth
        data = EntryAuth._trans(auth)
        self.entry.set_custom_property("auth", data)

    def get_auth(self, remember=False, reauth=False):
        user = User(self.username, self.password)
        self.auth = get_auth(user, self.auth, remember, reauth)
        if self.region is None:
            auth = get_extra_auth(self.auth, user.username)
            self.region = auth.region
            return auth
        return ExtraAuth(user.username, self.region, get_shard(self.region), self.auth)

    def _extract_auth(self, entry: KpEntry):
        if "auth" not in entry.custom_properties:
            return
        raw = entry.custom_properties["auth"]
        self._auth = EntryAuth._reverse(raw)

    def __init__(self, entry):
        try:
            self._extract_entry(entry)
        except AssertionError as e:
            raise EntryException(*e.args) from None
        except ValueError:
            raise EntryException("Alt not an integer") from None

    def _extract_entry(self, entry):
        assert isinstance(entry, KpEntry), "Missing entry"
        assert isinstance(entry.username, str), "Missing username"
        assert isinstance(entry.password, str), "Missing password"
        assert "alias" in entry.custom_properties, "Missing alias"
        assert "alt" in entry.custom_properties, "Missing alt"
        alias = entry.custom_properties["alias"]
        alt = entry.custom_properties["alt"]
        assert isinstance(alias, str), "Bad format alias"
        assert isinstance(alt, str), "Bad format alt"
        self._username = entry.username
        self._password = entry.password
        self._alias = alias
        self._alt = bool(int(alt))
        self.entry = entry
        self._extract_auth(entry)

    def __repr__(self) -> str:
        return f"Entry(username={self.username}, alias={self.alias}, alt={self.alt})"
