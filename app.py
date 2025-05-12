from flask import Blueprint, Flask, jsonify, redirect, request, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from src.utils.db import db
from src.routes.auth_routes import auth_bp
from config import Config, ProductionConfig
from src.routes.article_routes import article_bp

app = Flask(__name__)
CORS(app)

app.config.from_object(ProductionConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'][0] 
jwt = JWTManager(app)

api_bp = Blueprint('api', __name__, url_prefix='/api')

api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(article_bp)

app.register_blueprint(api_bp)


db.init_app(app)
with app.app_context():
    db.create_all()

allowed_origins = [
    'https://sari-front.vercel.app',
    'http://localhost:4200' 
]

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    print(f"Origin: {origin}")
    if origin in allowed_origins:
        response.headers['Access-Control-Allow-Origin'] = origin
    response.headers.add('Access-Control-Allow-credentials', True)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Ngrok-Skip-Browser-Warning')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def index():
    return jsonify({'message': 'Hello, World!'})

if __name__ == '__main__':
    app.run(debug=True)