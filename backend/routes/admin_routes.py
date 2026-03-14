from flask import Blueprint, jsonify, request 
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.company import Company
from models.student import Student
from models.drive import Drive
from models.application import Application
from models import db


admin_bp = Blueprint("admin", __name__)

def verify_admin(user_id):
    user = db.sesion.get(User, user_id)
    if user is None:
        return False
    if user.role != "admin":
        return False
    return True

@admin_bp.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():

    user_id = get_jwt_identity()
    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403
    total_students = Student.query.count()
    total_companies=Company.query.count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()

    return jsonify({
        "students": total_students,
        "companies": total_companies,
        "drives": total_drives,
        "applications": total_applications
    })


@admin_bp.route("/admin/approve_company/<int:company_id>", methods=["PUT"])
@jwt_required()
def approve_company(company_id):

    user_id = get_jwt_identity()

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    company = Company.db.sesion.get(Company, company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    company.approval_status = "Approved"

    db.session.commit()

    return jsonify({"message": "Company approved"})



@admin_bp.route("/admin/remove_company/<int:company_id>", methods=["DELETE"])
@jwt_required()
def remove_company(company_id):

    user_id = get_jwt_identity()

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    company = Company.db.sesion.get(Company, company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    db.session.delete(company)
    db.session.commit()

    return jsonify({"message": "Company removed"})




@admin_bp.route("/admin/search_company", methods=["GET"])
@jwt_required()
def search_company():

    user_id = get_jwt_identity()

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    name = request.args.get("name")

    if not name:
        return jsonify({"message": "Name parameter required"}), 400

    companies = Company.query.filter(
        Company.company_name.contains(name)
    ).all()

    result = []

    for c in companies:
        result.append({
            "id": c.id,
            "company_name": c.company_name,
            "website": c.website,
            "status": c.approval_status
        })

    return jsonify(result)



@admin_bp.route("/admin/search_student", methods=["GET"])
@jwt_required()
def search_student():

    user_id = get_jwt_identity()

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    name = request.args.get("name")

    students = Student.query.filter(
        Student.name.contains(name)
    ).all()

    result = []

    for s in students:
        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email
        })

    return jsonify(result)


@admin_bp.route("/admin/blacklist_user/<int:user_id>", methods=["PUT"])
@jwt_required()
def blacklist_user(user_id):

    admin_id = get_jwt_identity()

    if not verify_admin(admin_id):
        return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_active = False

    db.session.commit()

    return jsonify({"message": "User blacklisted"})

