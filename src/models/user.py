from utils.db import db
import uuid

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_role = db.Column(db.String(120), nullable=True)

    def __init__(self, name, lastName, password, email, user_role):
        self.name = name
        self.lastName = lastName
        self.email = email
        self.password = password
        self.user_role = user_role