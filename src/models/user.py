from utils.db import db
from sqlalchemy.dialects.mysql import BIGINT

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(BIGINT(unsigned = True), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_role = db.column(db.String(120), nullable=False)

    def __init__(self, name, lastName, password, email, user_role):
        self.name = name
        self.lastName = lastName
        self.email = email
        self.password = password
        self.user_rol = user_role