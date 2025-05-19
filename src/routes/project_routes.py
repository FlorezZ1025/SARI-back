import json
import uuid
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.supabase_functions import upload_pdf_to_supabase
from src.models.project import Project
from src.models.user import User
from src.services.pure import get_pure_projects
from src.utils.db import db

project_bp = Blueprint('projects', __name__, url_prefix='/projects')

@project_bp.route('/pure_projects', methods=['POST'])
@jwt_required()
def get_pure_projects_():
    user = json.loads(get_jwt_identity())
    email = user['email']
    request.json['email'] = email
    return get_pure_projects(request)

@project_bp.route('/create', methods=['POST'])
@jwt_required()
def create_project():
    user_token = json.loads(get_jwt_identity())
    user_id = user_token['id']

    new_id = str(uuid.uuid4())
    title = request.form.get('title')
    investigators = request.form.get('investigators')
    date = request.form.get('date')
    status = request.form.get('status')
    formulated_type = request.form.get('formulatedType')
    file_data = request.files.get('pdf')
    pdf_url = None

    if Project.query.filter(
            Project.id_user == user_id,
            Project.title == title).first():
        return make_response(jsonify({
            'message': 'Ya existe un proyecto con ese nombre',
            'statusCode': 400
        }), 400)
    bucket_name = 'support-pdfs'
    if file_data:
        pdf_url = upload_pdf_to_supabase(file_data, bucket_name)
    
    db.session.add(Project(
        id=new_id,
        id_user=user_id,
        title=title,
        investigators=investigators,
        date=date,
        status=status,
        formulated_type=formulated_type,
        pdf_url=pdf_url,
    ))
    db.session.commit()
    if pdf_url:
        res = make_response(jsonify({
            'message': 'Proyecto creado exitosamente',
            'statusCode': 201,
            'supportUrl': pdf_url,
            'idProject': new_id
        }), 201)
    else:
        res = make_response(jsonify({
            'message': 'Proyecto creado exitosamente',
            'statusCode': 201,
            'idProject': new_id
        }), 201)
    return res

@project_bp.route('/delete', methods=['POST'])
@jwt_required()
def delete_project():
    user = json.loads(get_jwt_identity())
    user_id = user['id']
    project_id = request.json.get('id')
    project = Project.query.filter_by(id=project_id, id_user=user_id).first()

    if not project:
        return make_response(jsonify({
            'message': 'No se encontró el proyecto',
            'statusCode': 404
        }), 404)

    db.session.delete(project)
    db.session.commit()
    return make_response(jsonify({
        'message': 'Proyecto eliminado exitosamente',
        'statusCode': 200
    }), 200)

@project_bp.route('/get_all', methods=['GET'])
@jwt_required()
def get_all_projects():
    user = json.loads(get_jwt_identity())
    email = user['email']
    user = User.query.filter_by(email=email).first()
    projects = Project.query.filter_by(id_user=user.id).all()
    projects_list = []

    for project in projects:
        projects_list.append({
            'id': project.id,
            'title': project.title,
            'investigators': json.loads(project.investigators),
            'date': project.date,
            'status': project.status,
            'formulatedType': project.formulated_type,
            'supportUrl': project.pdf_url
        })
    res = make_response(jsonify(projects_list),200)
    return res