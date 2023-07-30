from typing import List, Union

from pykeepass import PyKeePass, create_database
from pykeepass.entry import Entry as KpEntry

from ValLib import User

from .auth import get_auth
from .entry import Entry, EntryException
from .singleton import SingletonMeta
from .storage import settingsPath


class EntryNotFoundException(BaseException):
    pass


class DatabaseEmptyException(BaseException):
    pass


class EncryptedDB(metaclass=SingletonMeta):
    db: PyKeePass

    def __init__(self, password=None) -> None:
        path = settingsPath / "users.db"
        if path.is_file():
            self.db = PyKeePass(str(path), password)
            return
        self.create(str(path), password)

    def create(self, path, password):
        self.db = create_database(path, password)

    def save_user(self, user, password, alias=""):
        try:
            entry = self.get_user(user)
        except EntryNotFoundException:
            entry = self.new_entry()
        entry.username = user
        entry.password = password
        entry.alias = alias
        entry.alt = False
        self.db.save()

    def set_alias(self, username, alias):
        entry = self.find_one(username=username)
        if not entry:
            return
        entry.alias = alias
        self.db.save()

    def set_alt(self, username, alt):
        entry = self.find_one(username=username)
        if not entry:
            return
        entry.alt = alt
        self.db.save()

    def find(self, *args, **kwargs) -> List[Entry]:
        entries = self.db.find_entries(title="Riot", *args, **kwargs)
        if entries is None:
            raise EntryNotFoundException
        custom_entries: List[Entry] = []
        for e in entries:
            custom_entries.append(Entry(e))
        return custom_entries

    def find_one(self, *args, **kwargs) -> Entry:
        entry = self.db.find_entries(title="Riot", first=True, *args, **kwargs)
        if entry is None:
            raise EntryNotFoundException
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
        if not entry:
            return alias
        return entry.username

    def get_users(self):
        entries = self.find()
        return [e.username for e in entries]

    def get_user(self, username):
        return self.find_one(username=username)

    def get_passwd(self, user):
        entry = self.get_user(user)
        if not entry:
            return None
        return entry.password

    def get_auth(self, user: Union[str, User], remember=False, reauth=False):
        if not isinstance(user, User):
            user = User(user, "")
        entry = self.find_one(username=user.username)
        user.password = entry.password
        auth = get_auth(user, entry.auth, remember, reauth)
        entry.auth = auth
        self.db.save()
        return auth

    def fix_database(self):
        entries = self.db.find_entries()
        if not entries:
            raise DatabaseEmptyException
        for entry in entries:
            self.fix_entry(entry)

    @staticmethod
    def fix_entry(entry: KpEntry):
        def custom_check(key: str):
            return key not in custom or not custom[key]

        custom = entry.custom_properties
        if not entry.username:
            if not entry.password:
                entry.delete()
                return
            entry.username = f"NoUsername{entry.ctime}"
        if not entry.password:
            entry.password = ""
        if custom_check("alias"):
            entry.set_custom_property("alias", entry.username)
        if custom_check("alt"):
            entry.set_custom_property("alt", str(int(False)))
