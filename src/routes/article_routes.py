import json
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.pure import get_pure_service


article_bp = Blueprint('articles', __name__, url_prefix='/articles')

@article_bp.route('/pure_articles', methods=['POST'])
@jwt_required()
def get_pure():
    user = json.loads(get_jwt_identity())
    print(user)
    email = user['email']
    request.json['email'] = email
    return get_pure_service(request)

@article_bp.route('/create', methods=['POST'])
@jwt_required()
def create_article():
    user = json.loads(get_jwt_identity())
    email = user['email']

    data = request.json
    
    title = data.get('title')
    authors = json.dump(data.get('authors'))
    date = data.get('date')
    state = data.get('state')

    res = make_response(jsonify({
        'message': 'Article created successfully',
        'statusCode': 200
    }))
    
    return 
