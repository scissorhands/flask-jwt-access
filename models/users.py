from db import db
from werkzeug.security import generate_password_hash as hash_pw, check_password_hash as check_pw

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    created_at = db.Column(
    	db.DateTime,
    	server_default = db.func.current_timestamp()
    )

    def __init__(self, name, email, password):
    	self.name = name
    	self.email = email
    	self.set_password(password)

    def set_password(self, pwd):
    	self.password = hash_pw(pwd)

    def check_password(self, pwd):
        return check_pw(self.password, pwd)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()