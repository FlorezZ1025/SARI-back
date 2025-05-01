import json
import uuid
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.article import Article
from models.user import User
from services.pure import get_pure_articles
from utils.db import db


article_bp = Blueprint('articles', __name__, url_prefix='/articles')

@article_bp.route('/pure_articles', methods=['POST'])
@jwt_required()
def get_pure_articles_():
    user = json.loads(get_jwt_identity())
    email = user['email']
    request.json['email'] = email
    return get_pure_articles(request)

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

    if Article.query.filter(
            Article.id_user == user.id,
            Article.title == title).first():
  
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
        'message': 'Artículo creado correctamente',
        'statusCode': 200,
        'idArticle': new_id,
    }))
    
    return  res

@article_bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_article():
    user = json.loads(get_jwt_identity())

    data = request.json
    id = data.get('id')

    article = Article.query.filter_by(id=id).first()
    
    if not article:
        return make_response(jsonify({
            'message': 'No existe un artículo con ese ID',
            'statusCode': 404
        }), 404)
    
    db.session.delete(article)
    db.session.commit()

    res = make_response(jsonify({
        'message': 'Artículo eliminado correctamente',
        'statusCode': 200,
    }))

    return res

@article_bp.route('/update', methods=['POST'])
@jwt_required()
def update_article():

    data = request.json
    id = data.get('id')
    title = data.get('title')
    authors = json.dumps(data.get('authors'))
    date = data.get('date')
    state = data.get('state')

    article = Article.query.filter_by(id=id).first()
    
    if not article:
        return make_response(jsonify({
            'message': 'No existe un artículo con ese ID',
            'statusCode': 404
        }), 404)
    
    article.title = title
    article.authors = authors
    article.date = date
    article.state = state

    db.session.commit()

    res = make_response(jsonify({
        'message': 'Artículo actualizado correctamente',
        'statusCode': 200,
    }))

    return res

@article_bp.route('/get_all', methods=['GET'])
@jwt_required()
def get_all_articles():
    
    user = json.loads(get_jwt_identity())
    email = user['email']
    user = User.query.filter_by(email=email).first()
    articles = Article.query.filter_by(id_user=user.id).all()
    articles_list = []

    for article in articles:
        articles_list.append({
            'id': article.id,
            'title': article.title,
            'authors': json.loads(article.authors),
            'date': article.date,
            'state': article.state,
            'hyperlink': article.hyperlink if article.hyperlink else 'No disponible'
        })
    res = make_response(jsonify({
        'message': 'Artículos obtenidos correctamente',
        'statusCode': 200,
        'data': articles_list
    }),200)

    return res