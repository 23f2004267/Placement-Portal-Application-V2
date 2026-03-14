from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.company import Company
from models.drive import Drive
from models.application import Application
from models.student import Student
from models import db


company_bp = Blueprint("company", __name__)



def verify_company(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return None

    if user.role != "company":
        return None

    company = Company.query.filter_by(user_id=user_id).first()

    if company is None:
        return None

    if company.approval_status != "Approved":
        return None

    return company



@company_bp.route("/company/dashboard", methods=["GET"])
@jwt_required()
def company_dashboard():

    user_id = get_jwt_identity()

    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    total_drives = Drive.query.filter_by(company_id=company.id).count()

    return jsonify({
        "company_name": company.company_name,
        "total_drives": total_drives
    })



@company_bp.route("/company/create_drive", methods=["POST"])
@jwt_required()
def create_drive():

    user_id = get_jwt_identity()

    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()

    job_title = data.get("job_title")
    job_description = data.get("job_description")
    salary = data.get("salary")

    drive = Drive(
        company_id=company.id,
        job_title=job_title,
        job_description=job_description,
        salary=salary,
        status="Pending"
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({"message": "Placement drive created"})


@company_bp.route("/company/my_drives", methods=["GET"])
@jwt_required()
def my_drives():

    user_id = get_jwt_identity()

    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    drives = Drive.query.filter_by(company_id=company.id).all()

    result = []

    for d in drives:
        result.append({
            "id": d.id,
            "job_title": d.job_title,
            "salary": d.salary,
            "status": d.status
        })

    return jsonify(result)



@company_bp.route("/company/applicants/<int:drive_id>", methods=["GET"])
@jwt_required()
def view_applicants(drive_id):

    user_id = get_jwt_identity()

    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    applications = Application.query.filter_by(drive_id=drive_id).all()

    result = []

    for app in applications:

        student = db.session.get(Student, app.student_id)

        result.append({
            "application_id": app.id,
            "student_name": student.name,
            "status": app.status
        })

    return jsonify(result)



@company_bp.route("/company/update_application/<int:app_id>", methods=["PUT"])
@jwt_required()
def update_application(app_id):

    user_id = get_jwt_identity()

    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()

    new_status = data.get("status")

    application = db.session.get(Application, app_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    application.status = new_status

    db.session.commit()

    return jsonify({"message": "Application status updated"})