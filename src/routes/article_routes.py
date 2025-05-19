import json
import uuid
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.supabase_functions import get_object_key_from_url, upload_pdf_to_supabase
from src.models.article import Article
from src.models.user import User
from src.services.pure import get_pure_articles
from src.utils.db import db
from src.utils.db import s3

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
    user_id = user_token['id']

    new_id = str(uuid.uuid4())
    title = request.form.get('title')
    authors = request.form.get('authors')
    date = request.form.get('date')
    state = request.form.get('state')
    file_data = request.files.get('pdf')

    if Article.query.filter(
            Article.id_user == user_id,
            Article.title == title).first():
  
        return make_response(jsonify({
            'message': 'Ya existe un articulo con ese nombre',
            'statusCode': 400
        }), 400)
    
    pdf_url = None
    bucket_name = 'evidences-pdfs'
    if file_data:
        pdf_url = upload_pdf_to_supabase(file_data, bucket_name)

    db.session.add(Article(
        id = new_id,
        id_user = user_id,
        title = title,
        authors = authors,
        date = date,
        state = state,
        pdf_url = pdf_url,
    ))

    db.session.commit()
    if pdf_url:
        res = make_response(jsonify({
            'message': 'Artículo creado correctamente',
            'statusCode': 200,
            'idArticle': new_id,
            'evidenceUrl': pdf_url
        }))
    else:
        res = make_response(jsonify({
            'message': 'Artículo creado correctamente',
            'statusCode': 200,
            'idArticle': new_id,
        }))
    
    return  res

@article_bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_article():
    data = request.json
    id = data.get('id')

    article = Article.query.filter_by(id=id).first()
    
    if not article:
        return make_response(jsonify({
            'message': 'No existe un artículo con ese ID',
            'statusCode': 404
        }), 404)
    if article.pdf_url:
            object_key = get_object_key_from_url(article.pdf_url)
            if object_key:
                s3.delete_object(Bucket='evidences-pdfs', Key=object_key)
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
    user_token = json.loads(get_jwt_identity())
    user_id = user_token['id']

    id = request.form.get('id') 
    title = request.form.get('title')
    authors = request.form.get('authors')
    date = request.form.get('date')
    state = request.form.get('state')
    file_data = request.files.get('pdf')

    article = Article.query.filter_by(id=id).first()
    print(id)
    print(article)
    pdf_url = article.pdf_url
    
    if Article.query.filter(
            Article.id != id,
            Article.id_user == user_id,
            Article.title == title).first():
  
        return make_response(jsonify({
            'message': 'Ya existe un articulo con ese nombre',
            'statusCode': 400
        }), 400)
    previous_url = article.pdf_url
    if file_data and previous_url:
        object_key = get_object_key_from_url(article.pdf_url)
        if object_key:
            s3.delete_object(Bucket='evidences-pdfs', Key=object_key)
            pdf_url = upload_pdf_to_supabase(file_data)
    elif file_data:
        pdf_url = upload_pdf_to_supabase(file_data)    
    
    article.title = title
    article.authors = authors
    article.date = date
    article.state = state
    article.pdf_url = pdf_url

    db.session.commit()
    if pdf_url:
        res = make_response(jsonify({
            'message': 'Artículo actualizado correctamente',
            'statusCode': 200,
            'evidenceUrl': pdf_url
        }))
    else:
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
            'hyperlink': article.hyperlink if article.hyperlink else 'No disponible',
            'evidenceUrl': article.pdf_url,
        })
    res = make_response(jsonify(articles_list),200)
    return res

@article_bp.route('/add_hyperlink', methods=['POST'])
@jwt_required()
def add_hyperlink():
    user = json.loads(get_jwt_identity())
    email = user['email']
    user = User.query.filter_by(email=email).first()
    data = request.json

    id = data.get('id')
    hyperlink = data.get('hyperlink')

    article = Article.query.filter_by(id=id).first()
    
    if not article:
        return make_response(jsonify({
            'message': 'No existe un artículo con ese ID',
            'statusCode': 404
        }), 404)
    
    article.hyperlink = hyperlink
    db.session.commit()

    res = make_response(jsonify(article.id),200)

    return res