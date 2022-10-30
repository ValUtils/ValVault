from pykeepass import create_database, PyKeePass

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

	def get_users(self):
		entries = self.db.find_entries(title="Riot")
		return [e.username for e in entries]

	def get_user(self, username):
		return self.db.find_entries(username=username, first=True)

	def get_passwd(self, user):
		entry = self.get_user(user)
		if (not entry): return None
		return entry.password
