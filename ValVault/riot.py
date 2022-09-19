import ssl
import requests
from typing import Any
from collections import OrderedDict
from requests.adapters import HTTPAdapter

from .exceptions import AuthException
from .structs import Auth, User
from .parsing import encodeJSON, magicDecode

platform = {
	"platformType": "PC",
	"platformOS": "Windows",
	"platformOSVersion": "10.0.19042.1.256.64bit",
	"platformChipset": "Unknown"
}

FORCED_CIPHERS = [
	'ECDHE-ECDSA-AES128-GCM-SHA256',
	'ECDHE-ECDSA-CHACHA20-POLY1305',
	'ECDHE-RSA-AES128-GCM-SHA256',
	'ECDHE-RSA-CHACHA20-POLY1305',
	'ECDHE+AES128',
	'RSA+AES128',
	'ECDHE+AES256',
	'RSA+AES256',
	'ECDHE+3DES',
	'RSA+3DES'
]

userAgent = "RiotClient/51.0.0.4429735.4429735 rso-auth (Windows;10;;Professional, x64)"

def getToken(uri: str):
	access_token = uri.split("access_token=")[1].split("&scope")[0]
	token_id = uri.split("id_token=")[1].split("&")[0]
	return access_token, token_id

def post(session: requests.Session, access_token, url):
	headers = {
		'Accept-Encoding': 'gzip, deflate, br',
		'Authorization': f'Bearer {access_token}',
	}
	r = session.post(url, headers=headers, json={})
	return magicDecode(r.text)

def setupSession() -> requests.Session:
	class SSLAdapter(HTTPAdapter):
		def init_poolmanager(self, *args: Any, **kwargs: Any) -> None:
			ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
			ctx.set_ciphers(':'.join(FORCED_CIPHERS))
			kwargs['ssl_context'] = ctx
			return super(SSLAdapter, self).init_poolmanager(*args, **kwargs)

	session = requests.session()
	session.headers = OrderedDict({
		"User-Agent": userAgent,
		"Accept-Language": "en-US,en;q=0.9",
		"Accept": "application/json, text/plain, */*"
	})
	session.mount('https://', SSLAdapter())
	return session

def authenticate(user: User):
	session = setupSession()

	setupAuth(session)

	access_token, id_token = getAuthToken(session, user)

	entitlements_token = getEntitlement(session, access_token)

	user_id = getUserInfo(session, access_token)

	session.close()

	auth = Auth(access_token, id_token, entitlements_token, user_id)

	return auth

def setupAuth(session: requests.Session):
	data = {
		'client_id': 'riot-client',
		'nonce': '1',
		'redirect_uri': 'http://localhost/redirect',
		'response_type': 'token id_token',
		'scope': 'account openid',
	}

	session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data)

def getAuthToken(session: requests.Session, user: User):
	data = {
		'type': 'auth',
		'username': user.username,
		'password': user.password
	}

	r = session.put(f'https://auth.riotgames.com/api/v1/authorization', json=data)
	data = r.json()
	if ("error" in data):
		raise AuthException(data['error'])
	uri = data['response']['parameters']['uri']
	access_token, id_token = getToken(uri)
	return [access_token, id_token]

def getEntitlement(session: requests.Session, access_token):
	data = post(session, access_token, "https://entitlements.auth.riotgames.com/api/token/v1")
	return data['entitlements_token']

def getUserInfo(session: requests.Session, access_token):
	data = post(session, access_token, "https://auth.riotgames.com/userinfo")
	return data['sub']

def getVersion():
	r = requests.get('https://valorant-api.com/v1/version')
	data = r.json()['data']
	return data["riotClientVersion"]

def makeHeaders(auth: Auth):
	return {
		'Accept-Encoding': 'gzip, deflate, br',
		'User-Agent': userAgent,
		'Authorization': f'Bearer {auth.access_token}',
		'X-Riot-Entitlements-JWT': auth.entitlements_token,
		'X-Riot-ClientPlatform': encodeJSON(platform),
		'X-Riot-ClientVersion': getVersion()
	}