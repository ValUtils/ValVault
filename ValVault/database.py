from pykeepass import create_database, PyKeePass
from pykeepass.entry import Entry as KpEntry
from typing import List

from .storage import settingsPath
from .entry import Entry, EntryException


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
        except EntryException:
            entry = self.new_entry()
        entry.username = user
        entry.password = password
        entry.alias = alias
        entry.alt = False
        self.db.save()

    def set_alias(self, username, alias):
        entry = self.find_one(username=username)
        if (not entry):
            return
        entry.alias = alias
        self.db.save()

    def set_alt(self, username, alt):
        entry = self.find_one(username=username)
        if (not entry):
            return
        entry.alt = alt
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
        return Entry(entry)

    def new_entry(self) -> Entry:
        entry = self.db.add_entry(self.db.root_group, "Riot", "", "")
        entry.set_custom_property("alias", "")
        entry.set_custom_property("alt", "0")
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
