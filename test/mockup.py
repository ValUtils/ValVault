from time import time
from typing import Dict, Optional

from pykeepass.entry import Entry as KpEntry


class EntryMockup(KpEntry):
    _custom_properties: Dict
    _username: Optional[str] = ""
    _password: Optional[str] = ""
    _deleted = False
    _ctime = time()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def custom_properties(self):
        return self._custom_properties

    @custom_properties.setter
    def custom_properties(self, value):
        self._custom_properties = value

    @property
    def ctime(self):
        return self._ctime

    def set_custom_property(self, key, value):
        self._custom_properties[key] = value

    def delete(self):
        self._deleted = True

    def __init__(self, username: Optional[str] = "user", password: Optional[str] = "password", alias: Optional[str] = "alias"):
        self.username = username
        self.password = password
        self.custom_properties = {}
        self.custom_properties["alias"] = alias
        self.custom_properties["alt"] = str(int(False))
