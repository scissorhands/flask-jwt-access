from flask import Flask
from flask_restful import Api, Resource, reqparse, request
from helpers.util import build_dsn
from config.database import config as dbconfig

# Resources
from resources.users import User,Register,Auth,ProtectedAccess
from resources.home import Home

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = build_dsn(
	dbconfig['host'],
	dbconfig['user'],
	dbconfig['password'],
	dbconfig['database']
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'MySecret'
api = Api(app)

@app.before_first_request
def create_tales():
	db.create_all()

api.add_resource(Home, '/')
api.add_resource(Register, '/users/register')
api.add_resource(Auth, '/auth')
api.add_resource(ProtectedAccess, '/users/access')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)