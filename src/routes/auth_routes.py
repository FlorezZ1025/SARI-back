from flask import Blueprint, make_response, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from utils.db import db
from models.user import User
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    return jsonify({'message': 'wow'})

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    name = data.get('name')
    lastName = data.get('lastName')
    email = data.get('email')
    password = data.get('password')
    user_role = data.get('role')
    
    if User.query.filter_by(email=email).first():
        return make_response(jsonify({'message': 'User already exists', 'statusCode': 400 }), 400)
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(name=name, 
                    lastName=lastName,
                    email=email,
                    password=hashed_password,
                    user_role=user_role)
    
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({'message': 'User created successfully', 'statusCode':201}), 201)
