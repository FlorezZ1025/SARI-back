from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.pure import get_pure_service


indicator_bp = Blueprint('indicators', __name__, url_prefix='/indicators')

@indicator_bp.route('/pure_articles', methods=['POST'])
@jwt_required()
def get_pure():
    user = get_jwt_identity()
    email = user['email']
    return get_pure_service(request)
