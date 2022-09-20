from dataclasses import dataclass

@dataclass
class User:
	username: str
	password: str

@dataclass
class Auth:
	access_token: str
	id_token: str
	entitlements_token: str
	user_id: str

@dataclass
class Settings:
	insecure: bool