from flask_restful import Resource, reqparse, request
from models.users import User
import jwt
import json
from config.jwt import config as jwtconf


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
				jwtoken = jwt.encode(payload, jwtconf['secret'], algorithm=jwtconf['algorythm'])
				return {"access_token": jwtoken.decode('utf-8')}, 200
			else:
				return {"message": "Invalid password"}, 401
		else:
			return {"message": "User does not exist"}, 401

class ProtectedAccess(Resource):
	def get(self):
		auth_header = request.headers.get('Authorization')
		if auth_header is not None and 'JWT ' in auth_header:
			try:
				jwtoken = auth_header.split()
				decoded = jwt.decode(jwtoken[1], jwtconf['secret'], algorithms=[jwtconf['algorythm']])
			except jwt.exceptions.DecodeError as e:
				return {"message": "Invalid signature" }, 400
			return {"user": decoded},200
		else:
			return {"message": "Access denied"}, 401