from typing import List, Optional, Union

from pykeepass import PyKeePass, create_database
from pykeepass.entry import Entry as KpEntry

from ValLib import User

from .auth import get_auth
from .debug import Level, log
from .entry import Entry
from .singleton import SingletonMeta
from .storage import settingsPath


class EntryNotFoundException(BaseException):
    pass


class DatabaseEmptyException(BaseException):
    pass


class EncryptedDB(metaclass=SingletonMeta):
    db: PyKeePass

    def __init__(self, password: Optional[str]) -> None:
        path = settingsPath / "users.db"
        if path.is_file():
            log(Level.DEBUG, "Init disk database", "database")
            self.db = PyKeePass(str(path), password)
            return
        log(Level.INFO, "Create new database", "database")
        self.create(str(path), password)

    def create(self, path: str, password: Optional[str]):
        self.db = create_database(path, password)

    def save_user(self, user: str, password: str, alias=""):
        log(Level.DEBUG, f"Save new user {user} as {alias}", "database")
        try:
            entry = self.get_user(user)
        except EntryNotFoundException:
            entry = self.new_entry()
        entry.username = user
        entry.password = password
        entry.alias = alias
        entry.alt = False
        self.db.save()

    def find(self, *args, **kwargs) -> List[Entry]:
        log(Level.DEBUG, f"Finding users {args=} {kwargs=}", "database")
        entries = self.db.find_entries(title="Riot", *args, **kwargs)
        if entries is None:
            raise EntryNotFoundException
        custom_entries: List[Entry] = []
        for e in entries:
            custom_entries.append(Entry(e))
        return custom_entries

    def find_one(self, *args, **kwargs) -> Entry:
        log(Level.FULL, f"Find one {args=} {kwargs=}", "database")
        entry = self.db.find_entries(title="Riot", first=True, *args, **kwargs)
        if entry is None:
            raise EntryNotFoundException
        return Entry(entry)

    def new_entry(self) -> Entry:
        log(Level.FULL, f"Create new Entry for database", "database")
        entry = self.db.add_entry(self.db.root_group, "Riot", "", "")
        entry.set_custom_property("alias", "")
        entry.set_custom_property("alt", "0")
        return Entry(entry)

    @property
    def aliases(self):
        log(Level.DEBUG, "Getting aliases", "database")
        entries = self.find()
        return [e.alias or e.username for e in entries]

    @property
    def users(self):
        log(Level.DEBUG, "Get usernames")
        entries = self.find()
        return [e.username for e in entries]

    def get_name(self, alias: str) -> str:
        log(Level.DEBUG, f"Get name for {alias}", "database")
        entry = self.find_one(string={"alias": alias})
        if not entry:
            return alias
        return entry.username

    def get_user(self, username: str):
        log(Level.DEBUG, f"Get Entry for {username}", "database")
        return self.find_one(username=username)

    def get_passwd(self, username: str):
        log(Level.DEBUG, f"Get password for {username}", "database")
        entry = self.get_user(username)
        if not entry:
            return None
        return entry.password

    def get_auth(self, user: Union[str, User], remember=False, reauth=False):
        if not isinstance(user, User):
            user = User(user, "")
        log(Level.DEBUG,
            f"Get auth for {user.username} {remember=} {reauth=}", "database")
        entry = self.find_one(username=user.username)
        user.password = entry.password
        auth = get_auth(user, entry.auth, remember, reauth)
        entry.auth = auth
        self.db.save()
        return auth

    def set_alias(self, username: str, alias: str):
        log(Level.DEBUG, f"Set {username} alias to {alias}", "database")
        entry = self.find_one(username=username)
        if not entry:
            return
        entry.alias = alias
        self.db.save()

    def set_alt(self, username: str, alt: bool):
        log(Level.DEBUG, f"Set {username} alt to {alt}", "database")
        entry = self.find_one(username=username)
        if not entry:
            return
        entry.alt = alt
        self.db.save()

    def fix_database(self):
        log(Level.DEBUG, "Fixing database", "database")
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
                log(Level.VERBOSE, "Deleting broken entry", "database")
                entry.delete()
                return
            entry.username = f"NoUsername{entry.ctime}"
        if not entry.password:
            log(Level.VERBOSE, "Setting password for broken entry", "database")
            entry.password = ""
        if custom_check("alias"):
            log(Level.VERBOSE, "Setting alias for broken entry", "database")
            entry.set_custom_property("alias", entry.username)
        if custom_check("alt"):
            log(Level.VERBOSE, "Setting alt for broken entry", "database")
            entry.set_custom_property("alt", str(int(False)))
