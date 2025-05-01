import json
import uuid
from flask import Blueprint, jsonify, make_response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.article import Article
from models.user import User
from services.pure import get_pure_projects
from utils.db import db