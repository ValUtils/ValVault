import json
import jwt
import base64

from .exceptions import DecodeException

def encodeJSON( data ):
	str = json.dumps(data).encode("utf-8")
	return base64.b64encode(str).decode("utf-8")

def decodeJSON( data ):
	str = base64.b64decode(data.encode("utf-8"))
	return json.loads(str)

def magicDecode( string: str ):
	try:
		return json.loads(string)
	except:
		pass
	try:
		return jwt.decode(string, options={"verify_signature": False})
	except:
		pass
	raise DecodeException(string)
