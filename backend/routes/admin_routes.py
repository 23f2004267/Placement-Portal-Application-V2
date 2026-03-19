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
    user = db.session.get(User, user_id)
    if user is None:
        return False
    if user.role != "admin":
        return False
    return True

@admin_bp.route("/admin/dashboard", methods=["GET"])
@jwt_required()
def admin_dashboard():

    user_id = int(get_jwt_identity())
    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()

    print("ADMIN DASHBOARD CHECK")
    print("Total students:", total_students)
    print("Total companies:", total_companies)
    print("Total drives:", total_drives)
    print("Total applications:", total_applications)

    return jsonify({
        "students": total_students,
        "companies": total_companies,
        "drives": total_drives,
        "applications": total_applications
    })


@admin_bp.route("/admin/companies", methods=["GET"])
@jwt_required()
def view_companies():

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    companies = Company.query.all()

    result = []

    for c in companies:
        result.append({
            "id": c.id,
            "company_name": c.company_name,
            "website": c.website,
            "status": c.approval_status
        })

    print("ADMIN VIEW COMPANIES")
    print("Companies fetched:", len(result))
    print(result)

    return jsonify(result)


@admin_bp.route("/admin/students", methods=["GET"])
@jwt_required()
def view_students():

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    students = Student.query.all()

    result = []

    for s in students:
        user = db.session.get(User, s.user_id)

        is_active = True
        if user:
            is_active = user.is_active

        result.append({
            "id": s.id,
            "user_id": s.user_id,
            "name": s.name,
            "email": s.email,
            "is_active": is_active
        })

    return jsonify(result)


@admin_bp.route("/admin/drives", methods=["GET"])
@jwt_required()
def view_all_drives():

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    drives = Drive.query.all()

    result = []

    for d in drives:
        company = db.session.get(Company, d.company_id)

        company_name = ""
        if company:
            company_name = company.company_name

        result.append({
            "id": d.id,
            "company_name": company_name,
            "job_title": d.job_title,
            "salary": d.salary,
            "status": d.status
        })

    return jsonify(result)


@admin_bp.route("/admin/approve_drive/<int:drive_id>", methods=["PUT"])
@jwt_required()
def approve_drive(drive_id):

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    drive = db.session.get(Drive, drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.status = "Approved"
    db.session.commit()

    return jsonify({"message": "Drive approved"})


@admin_bp.route("/admin/approve_company/<int:company_id>", methods=["PUT"])
@jwt_required()
def approve_company(company_id):

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    company = db.session.get(Company, company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    company.approval_status = "Approved"

    db.session.commit()

    return jsonify({"message": "Company approved"})


@admin_bp.route("/admin/remove_company/<int:company_id>", methods=["DELETE"])
@jwt_required()
def remove_company(company_id):

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    company = db.session.get(Company, company_id)

    if not company:
        return jsonify({"message": "Company not found"}), 404

    drives = Drive.query.filter_by(company_id=company.id).all()

    for drive in drives:
        applications = Application.query.filter_by(drive_id=drive.id).all()

        for app in applications:
            db.session.delete(app)

        db.session.delete(drive)

    company_user = db.session.get(User, company.user_id)

    db.session.delete(company)

    if company_user:
        db.session.delete(company_user)

    db.session.commit()

    return jsonify({"message": "Company removed"})


@admin_bp.route("/admin/search_company", methods=["GET"])
@jwt_required()
def search_company():

    user_id = int(get_jwt_identity())

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

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    name = request.args.get("name")

    students = Student.query.filter(
        Student.name.contains(name)
    ).all()

    result = []

    for s in students:
        user = db.session.get(User, s.user_id)

        is_active = True
        if user:
            is_active = user.is_active

        result.append({
            "id": s.id,
            "user_id": s.user_id,
            "name": s.name,
            "email": s.email,
            "is_active": is_active
        })

    return jsonify(result)


@admin_bp.route("/admin/blacklist_user/<int:user_id>", methods=["PUT"])
@jwt_required()
def blacklist_user(user_id):

    admin_id = int(get_jwt_identity())

    if not verify_admin(admin_id):
        return jsonify({"message": "Access denied"}), 403

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_active = False

    db.session.commit()

    return jsonify({"message": "User blacklisted"})