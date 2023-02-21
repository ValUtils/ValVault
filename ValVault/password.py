from pykeepass import create_database, PyKeePass
from pykeepass.entry import Entry as KpEntry
from typing import List

from .storage import settingsPath


class Entry():
    entry: KpEntry
    username: str = ""
    password: str = ""
    alias: str = ""
    alt: bool = False

    def set_custom_property(self, key, value):
        self.entry.set_custom_property(key, value)

    def __init__(self, entry: KpEntry):
        assert isinstance(entry.username, str)
        assert isinstance(entry.password, str)
        assert "alias" in entry.custom_properties
        assert isinstance(entry.custom_properties["alias"], str)
        assert "alt" in entry.custom_properties
        assert isinstance(entry.custom_properties["alt"], str)
        self.username = entry.username
        self.password = entry.password
        self.alias = entry.custom_properties["alias"]
        self.alt = bool(int(entry.custom_properties["alt"]))
        self.entry = entry

    def __repr__(self) -> str:
        return f"Entry(username={self.username}, alias={self.alias}, alt={self.alt})"


class EncryptedDB:
    db: PyKeePass

    def __init__(self, password=None) -> None:
        path = settingsPath / "users.db"
        if (path.is_file()):
            self.db = PyKeePass(str(path), password)
            return
        self.create(str(path), password)

    def create(self, path, password):
        self.db = create_database(path, password)

    def save_user(self, user, password, alias=""):
        try:
            entry = self.get_user(user)
            entry.password = password
        except AssertionError:
            entry = self.db.add_entry(
                self.db.root_group, "Riot", user, password)
        entry.set_custom_property("alias", alias)
        entry.set_custom_property("alt", "0")
        self.db.save()

    def set_alias(self, username, alias):
        entry = self.find_one(username=username)
        if (not entry):
            return
        entry.set_custom_property("alias", alias)
        self.db.save()

    def set_alt(self, username, alt):
        entry = self.find_one(username=username)
        if (not entry):
            return
        alt_str = str(int(alt))
        entry.set_custom_property("alt", alt_str)
        self.db.save()

    def find(self, *args, **kwargs) -> List[Entry]:
        entries = self.db.find_entries(title="Riot", *args, **kwargs)
        if (entries is None):
            return []
        custom_entries: List[Entry] = []
        for e in entries:
            custom_entries.append(Entry(e))
        return custom_entries

    def find_one(self, *args, **kwargs) -> Entry:
        entry = self.db.find_entries(title="Riot", first=True, *args, **kwargs)
        assert isinstance(entry, KpEntry)
        return Entry(entry)

    def get_aliases(self):
        entries = self.find()
        return [e.alias or e.username for e in entries]

    def get_name(self, alias) -> str:
        entry = self.find_one(string={"alias": alias})
        if (not entry):
            return alias
        return entry.username

    def get_users(self):
        entries = self.find()
        return [e.username for e in entries]

    def get_user(self, username):
        return self.find_one(username=username)

    def get_passwd(self, user):
        entry = self.get_user(user)
        if (not entry):
            return None
        return entry.password
