from flask import Blueprint, Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from utils.db import db
from routes.auth_routes import auth_bp
from config import Config, DevelopmentConfig
from routes.indicators_routes import indicator_bp
from flask import jsonify

app = Flask(__name__)
CORS(app) 

app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'][0]  # Ajustar la URI de la base de datos

jwt = JWTManager(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(indicator_bp)
app.register_blueprint(api_bp)

db.init_app(app)
with app.app_context():
    db.create_all()

@app.after_request
def add_cors_headers(response):
    # response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-credentials', True)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    # response.headers.add('Access-Control-Allow-Credentials', 'true')  # Para cookies
    return response

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])