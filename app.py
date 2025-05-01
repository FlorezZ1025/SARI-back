from flask import Blueprint, Flask, jsonify, redirect, request, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from src.utils.db import db
from src.routes.auth_routes import auth_bp
from config import Config
from src.routes.indicators_routes import indicator_bp

app = Flask(__name__)
CORS(app)
# , resources={r"/*": {"origins": ["https://sari-front_vercel.app", "http://localhost:4200"]}} 


app.config.from_object(Config)

jwt = JWTManager(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(indicator_bp)

app.register_blueprint(api_bp)


db.init_app(app)
with app.app_context():
    db.create_all()

allowed_origins = [
    'https://sari-front.vercel.app',
    'http://localhost:4200'  # o el puerto de tu front local
]

@app.after_request
def add_cors_headers(response):
    # 
    origin = request.headers.get('Origin')
    print(f"Origin: {origin}")
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers.add('Access-Control-Allow-credentials', True)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    # response.headers.add('Access-Control-Allow-Credentials', 'true')  # Para cookies
    return response

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=True)