import json
import uuid
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
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
        })
    res = make_response(jsonify(projects_list),200)
    return res