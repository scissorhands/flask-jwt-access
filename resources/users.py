from flask_restful import Resource, reqparse, request
from models.users import User
from libraries.jwtlib import JWTLib
jwtlib = JWTLib()

class Register(Resource):
	parser = reqparse.RequestParser(bundle_errors=True)
	parser.add_argument(
		'name', 
		type=str,
		required=True, 
		help='name field is required'
	)
	parser.add_argument(
		'email', 
		type=str,
		required=True, 
		help='email field is required'
	)
	parser.add_argument(
		'password', 
		type=str,
		required=True, 
		help='password field is required'
	)

	def post(self):
		data = Register.parser.parse_args()
		user = User.find_by_email(data['email'])
		if(user):
			return {"message": "User already exists"}, 400
		else:
			try:
				user = User(**data)
				user.save()
				return {"user":user.to_json()}, 201
			except Exception as e:
				return {"message": "There was an error trying to insert user"}, 500

class Auth(Resource):
	parser = reqparse.RequestParser(bundle_errors=True)
	parser.add_argument(
		'email', 
		type=str,
		required=True, 
		help='email field is required'
	)
	parser.add_argument(
		'password', 
		type=str,
		required=True, 
		help='password field is required'
	)
	def post(self):
		data = Auth.parser.parse_args()
		user = User.find_by_email(data['email'])
		if user:
			if user.check_password(data['password']):
				payload = user.to_json()
				token = jwtlib.encrypt(payload)
				return {"access_token": token}, 200
			else:
				return {"message": "Invalid password"}, 401
		else:
			return {"message": "User does not exist"}, 401

class ProtectedAccess(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument(
		'additional_content', 
		type=str,
		required=True, 
		help='additional_content field is required'
	)

	def get(self):
		try:
			payload = jwtlib.decrypt_auth()
			return {"user": payload}, 200
		except Exception as e:
			return {"message": str(e)}, 401

	def post(self):
		data = ProtectedAccess.parser.parse_args()
		try:
			payload = jwtlib.decrypt_auth()
			payload['additional_content'] = data['additional_content']
			token = jwtlib.encrypt(payload)
			return {"access_token": token}, 200
		except Exception as e:
			return {"message": str(e)}, 401