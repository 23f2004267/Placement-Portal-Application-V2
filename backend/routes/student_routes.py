from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

student_bp = Blueprint("student", __name__)

@student_bp.route("/student/dashboard", methods=["GET"])
@jwt_required()
def student_dashboard():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user.role != "student":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "message": "Student Dashboard Access"
    })