from flask import Blueprint, Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from routes.auth_routes import auth_bp
from config import Config

app = Flask(__name__)
CORS(app) 


app.config.from_object(Config)

jwt = JWTManager(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(auth_bp)

app.register_blueprint(api_bp)


db.init_app(app)
with app.app_context():
    db.create_all()