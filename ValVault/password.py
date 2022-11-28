from pykeepass import create_database, PyKeePass
from pykeepass.entry import Entry

from .storage import settingsPath

class EncryptedDB:
	db: PyKeePass

	def __init__(self, password = None) -> None:
		path = settingsPath / "users.db"
		if (path.is_file()):
			self.db = PyKeePass(str(path), password)
			return
		self.create(str(path), password)

	def create(self, path, password):
		self.db = create_database(path, password)

	def save_user(self, user, password):
		entry = self.get_user(user)
		if (entry):
			entry.password = password
			self.db.save()
			return
		self.db.add_entry(self.db.root_group, "Riot", user, password)
		self.db.save()

	def find(self, *args, **kwargs) -> list[Entry]:
		return self.db.find_entries(title="Riot", *args, **kwargs)

	def find_one(self, *args, **kwargs) -> Entry:
		return self.db.find_entries(title="Riot", first=True, *args, **kwargs)

	def get_users(self):
		entries = self.find()
		return [e.username for e in entries]

	def get_user(self, username):
		return self.find_one(username=username)

	def get_passwd(self, user):
		entry = self.get_user(user)
		if (not entry): return None
		return entry.password
