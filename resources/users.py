from flask_restful import Resource, reqparse, request
from models.users import User
import json

class UserAuth(Resource):
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
		data = UserAuth.parser.parse_args()
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