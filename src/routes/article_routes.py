import json
import uuid
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.article import Article
from models.user import User
from services.pure import get_pure_service
from utils.db import db


article_bp = Blueprint('articles', __name__, url_prefix='/articles')

@article_bp.route('/pure_articles', methods=['POST'])
@jwt_required()
def get_pure():
    user = json.loads(get_jwt_identity())
    email = user['email']
    request.json['email'] = email
    return get_pure_service(request)

@article_bp.route('/create', methods=['POST'])
@jwt_required()
def create_article():
    user_token = json.loads(get_jwt_identity())
    email = user_token['email']
    user = User.query.filter_by(email=email).first()
    data = request.json

    new_id = str(uuid.uuid4())
    title = data.get('title')
    authors = json.dumps(data.get('authors'))
    date = data.get('date')
    state = data.get('state')

    if Article.query.filter_by(title=title).first():
        return make_response(jsonify({
            'message': 'Ya existe un articulo con ese nombre',
            'statusCode': 400
        }), 400)
    
    db.session.add(Article(
        id = new_id,
        id_user = user.id,
        title = title,
        authors = authors,
        date = date,
        state = state
    ))

    db.session.commit()

    res = make_response(jsonify({
        'message': 'Article created successfully',
        'statusCode': 200,
        'idArticle': new_id,
    }))
    
    return  res
