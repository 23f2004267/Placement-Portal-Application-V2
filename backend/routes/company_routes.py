from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

company_bp = Blueprint("company", __name__)

@company_bp.route("/company/dashboard", methods=["GET"])
@jwt_required()
def company_dashboard():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user.role != "company":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "message": "Company Dashboard Access"
    })