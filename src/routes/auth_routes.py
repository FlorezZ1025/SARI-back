from flask import Blueprint, make_response, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_access_cookies
from utils.db import db
from models.user import User
import bcrypt
import json

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()

        if not user:
            return make_response(jsonify({'message': 'Email no registrado', 'statusCode': 404}), 404)


        if not user.password or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return make_response(jsonify({'message': 'Contraseña incorrecta', 'statusCode': 401}), 401)

        res_user = {'email': user.email, 'name':user.name, 'lastName':user.last_name, 'role': user.role}
        
        
        access_token = create_access_token(identity=json.dumps(res_user))
        res = make_response(jsonify({
                'token':access_token,
                'statusCode': 200,
                'message':'Inicio de sesion exitoso'}), 200)
        return res
        
    except Exception as e:
        print(e)
        return make_response(jsonify({'message': 'Error en el servidor', 'statusCode': 500}), 500)
    
  
 

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    
    name = data.get('name').lower()
    last_name = data.get('lastName').lower()
    email = data.get('email')
    password = data.get('password')
    user_role = data.get('role')
    
    if User.query.filter_by(email=email).first():
        return make_response(jsonify({'message': 'Email ya registrado', 'statusCode': 400 }), 400)
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')

    new_user = User(name=name, 
                    last_name=last_name,
                    email=email,
                    password=hashed_password,
                    role=user_role)
    
    db.session.add(new_user)
    db.session.commit()

    return make_response(jsonify({'message': 'Usuario creado exitosamente', 'statusCode':201}), 201)
