from config.app import config as appconfig, os
import jwt
from flask_restful import request

if( appconfig['ENV'] == 'development' ):
	from config.jwt import config as jwtconf

class JWTLib():
	def __init__(self):
		if( appconfig['ENV'] == 'development' ):
			self.secret = jwtconf['secret']
			self.algorythm = jwtconf['algorythm']
		else:
			self.secret = os.environ.get('JWT_SECRET')
			self.algorythm = os.environ.get('JWT_ALGORYTHM')

	def encrypt(self, payload):
		jwtoken = jwt.encode(
			payload, 
			self.secret, 
			algorithm=self.algorythm
		)
		return jwtoken.decode('utf-8')

	def decrypt(self, token):
		return jwt.decode(
			token, 
			self.secret, 
			algorithms=[self.algorythm]
		)

	def decrypt_auth(self):
		auth_header = request.headers.get('Authorization')
		if auth_header is not None and 'JWT ' in auth_header:
			try:
				jwtoken = auth_header.split()
				decoded = self.decrypt(jwtoken[1])
			except jwt.exceptions.DecodeError as e:
				raise Exception("Invalid signature")
			return decoded
		else:
			raise Exception("Invalid header credentials")