from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user.role != "admin":
        return jsonify({"message": "Access denied"}), 403

    return jsonify({
        "message": "Admin Dashboard Access"
    })