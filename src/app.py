from flask import Blueprint, Config, Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from utils.db import db

app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

jwt = JWTManager(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')

app.register_blueprint(api_bp)

db.init_app(app)
with app.app_context():
    db.create_all()