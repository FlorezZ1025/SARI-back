from flask import Blueprint, Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from src.utils.db import db
from src.routes.auth_routes import auth_bp
from src.config import Config
from src.routes.indicators_routes import indicator_bp

app = Flask(__name__)
CORS(app) 


app.config.from_object(Config)

jwt = JWTManager(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(indicator_bp)

app.register_blueprint(api_bp)


# @app.route('/')
# def index():
#     return 'SARIs BACK is running!'

db.init_app(app)
with app.app_context():
    db.create_all()