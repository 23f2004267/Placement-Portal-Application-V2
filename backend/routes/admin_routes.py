from flask import Blueprint, jsonify, request 
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.company import Company
from models.student import Student
from models.drive import Drive
from models.application import Application
from models.placement import Placement
from models import db
from extensions import cache


admin_bp = Blueprint("admin", __name__)

def verify_admin(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return False
    if user.role != "admin" or user.is_active == False:
        return False
    return True


@admin_bp.route("/admin/dashboard", methods=["GET"])
@cache.cached(timeout=60)
@jwt_required()
def admin_dashboard():

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = Drive.query.count()
    total_applications = Application.query.count()

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

    companies = Company.query.filter_by().all()

    result = []

    for c in companies:
        user = db.session.get(User, c.user_id)

        if user and user.is_active == False:
            continue

        result.append({
            "id": c.id,
            "company_name": c.company_name,
            "website": c.website,
            "status": c.approval_status,
            "user_id": c.user_id
        })

    return jsonify(result)

    result = []

    for c in companies:
        result.append({
            "id": c.id,
            "company_name": c.company_name,
            "website": c.website,
            "status": c.approval_status,
            "user_id": c.user_id 
        })

    return jsonify(result)


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

    user = db.session.get(User, company.user_id)

    if user:
        user.is_active = False

    db.session.commit()

    return jsonify({"message": "Company removed (blacklisted)"})


@admin_bp.route("/admin/search_company", methods=["GET"])
@jwt_required()
def search_company():

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    name = request.args.get("name", "")

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

        if user and user.is_active == False:
            continue

        result.append({
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "user_id": s.user_id,
            "is_active": user.is_active if user else True,
            "resume": s.resume
        })

    return jsonify(result)

@admin_bp.route("/admin/search_student", methods=["GET"])
@jwt_required()
def search_student():

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    name = request.args.get("name", "")

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

    admin_id = int(get_jwt_identity())

    if not verify_admin(admin_id):
        return jsonify({"message": "Access denied"}), 403

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    user.is_active = False
    db.session.commit()

    return jsonify({"message": "User blacklisted"})



@admin_bp.route("/admin/placements", methods=["GET"])
@jwt_required()
def view_placements():

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    placements = Placement.query.all()

    result = []

    for p in placements:

        student = db.session.get(Student, p.student_id)
        company = db.session.get(Company, p.company_id)

        result.append({
            "placement_id": p.id,
            "student_name": student.name if student else "",
            "company_name": company.company_name if company else "",
            "position": p.position,
            "salary": p.salary
        })

    return jsonify(result)

@admin_bp.route("/admin/drives", methods=["GET"])
@jwt_required()
def view_drives():

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    drives = Drive.query.all()

    result = []

    for d in drives:
        company = db.session.get(Company, d.company_id)

        result.append({
            "id": d.id,
            "company_name": company.company_name if company else "",
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

@admin_bp.route("/admin/remove_drive/<int:drive_id>", methods=["DELETE"])
@jwt_required()
def remove_drive(drive_id):

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    drive = db.session.get(Drive, drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    db.session.delete(drive)
    db.session.commit()

    return jsonify({"message": "Drive removed"})
    
@admin_bp.route("/admin/complete_drive/<int:drive_id>", methods=["PUT"])
@jwt_required()
def complete_drive(drive_id):

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    drive = db.session.get(Drive, drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.status = "Completed"
    db.session.commit()

    return jsonify({"message": "Drive marked as completed"})

@admin_bp.route("/admin/applications", methods=["GET"])
@jwt_required()
def view_all_applications():

    user_id = int(get_jwt_identity())

    if not verify_admin(user_id):
        return jsonify({"message": "Access denied"}), 403

    applications = Application.query.all()

    result = []

    for app in applications:
        student = db.session.get(Student, app.student_id)
        drive = db.session.get(Drive, app.drive_id)
        company = db.session.get(Company, drive.company_id) if drive else None

        result.append({
            "application_id": app.id,
            "student_name": student.name if student else "",
            "branch": student.branch if student else "",
            "resume": student.resume if student else "",
            "company_name": company.company_name if company else "",
            "job_title": drive.job_title if drive else "",
            "status": app.status
        })

    return jsonify(result)