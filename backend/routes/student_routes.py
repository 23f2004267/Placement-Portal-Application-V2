from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.student import Student
from models.drive import Drive
from models.application import Application
from models.company import Company
from models import db
from extensions import cache


student_bp = Blueprint("student", __name__)




def verify_student(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return None

    if user.role != "student":
        return None

    student = Student.query.filter_by(user_id=user_id).first()

    return student



@student_bp.route("/student/dashboard", methods=["GET"])
@jwt_required()
def student_dashboard():

    user_id = get_jwt_identity()

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    total_applications = Application.query.filter_by(student_id=student.id).count()

    return jsonify({
        "student_name": student.name,
        "applications": total_applications
    })


@student_bp.route("/student/drives", methods=["GET"])
@jwt_required()
@cache.cached(timeout=60, query_string=True)
def view_drives():

    user_id = get_jwt_identity()

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    drives = Drive.query.filter_by(status="Approved").all()

    result = []

    for d in drives:

        company = db.session.get(Company, d.company_id)

        result.append({
            "drive_id": d.id,
            "company_name": company.company_name,
            "job_title": d.job_title,
            "salary": d.salary
        })

    return jsonify(result)




@student_bp.route("/student/search_drives", methods=["GET"])
@jwt_required()
def search_drives():

    user_id = get_jwt_identity()

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    title = request.args.get("title")

    drives = Drive.query.filter(
        Drive.job_title.contains(title),
        Drive.status == "Approved"
    ).all()

    result = []

    for d in drives:

        company = db.session.get(Company, d.company_id)

        result.append({
            "drive_id": d.id,
            "company": company.company_name,
            "job_title": d.job_title,
            "salary": d.salary
        })

    return jsonify(result)



@student_bp.route("/student/apply/<int:drive_id>", methods=["POST"])
@jwt_required()
def apply_drive(drive_id):

    user_id = get_jwt_identity()

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    drive = db.session.get(Drive, drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    if drive.status != "Approved":
        return jsonify({"message": "Drive not available for application"}), 400
    
    existing_application = Application.query.filter_by(
        student_id=student.id,
        drive_id=drive_id
    ).first()

    if existing_application:
        return jsonify({"message": "Already applied"}), 400

    application = Application(
        student_id=student.id,
        drive_id=drive_id,
        status="Applied"
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({"message": "Application submitted"})



@student_bp.route("/student/my_applications", methods=["GET"])
@jwt_required()
def my_applications():

    user_id = get_jwt_identity()

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    applications = Application.query.filter_by(student_id=student.id).all()

    result = []

    for a in applications:

        drive = db.session.get(Drive, a.drive_id)

        result.append({
            "application_id": a.id,
            "job_title": drive.job_title,
            "status": a.status
        })

    return jsonify(result)