from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.student import Student
from models.drive import Drive
from models.application import Application
from models.company import Company
from models.placement import Placement
from models import db
from datetime import date
import os


student_bp = Blueprint("student", __name__)

def verify_student(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return None

    if user.role != "student":
        return None

    if user.is_active == False:
        return None

    student = Student.query.filter_by(user_id=user_id).first()

    return student


@student_bp.route("/student/dashboard", methods=["GET"])
@jwt_required()
def student_dashboard():

    user_id = int(get_jwt_identity())

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    total_applications = Application.query.filter_by(student_id=student.id).count()

    return jsonify({
        "student_name": student.name,
        "applications": total_applications,
        "resume": student.resume if student.resume else ""
    })


@student_bp.route("/student/drives", methods=["GET"])
@jwt_required()
def view_drives():

    user_id = int(get_jwt_identity())

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    drives = Drive.query.filter_by(status="Approved").all()

    result = []

    for d in drives:
        company = db.session.get(Company, d.company_id)

        if company:
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

    user_id = int(get_jwt_identity())

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

        if company:
            result.append({
                "drive_id": d.id,
                "company_name": company.company_name,
                "job_title": d.job_title,
                "salary": d.salary
            })

    return jsonify(result)


@student_bp.route("/student/drive/<int:drive_id>", methods=["GET"])
@jwt_required()
def drive_details(drive_id):

    user_id = int(get_jwt_identity())

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({"message": "Access denied"}), 403

    student = None

    if user.role == "student":
        student = verify_student(user_id)
        if not student:
            return jsonify({"message": "Access denied"}), 403

    drive = db.session.get(Drive, drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    if user.role == "student" and drive.status not in ["Approved", "Completed"]:
        return jsonify({"message": "Drive not available"}), 400

    company = db.session.get(Company, drive.company_id)

    company_name = ""
    if company:
        company_name = company.company_name

    return jsonify({
        "drive_id": drive.id,
        "company_name": company_name,
        "job_title": drive.job_title,
        "job_description": drive.job_description,
        "salary": drive.salary,
        "status": drive.status
    })


@student_bp.route("/student/apply/<int:drive_id>", methods=["POST"])
@jwt_required()
def apply_drive(drive_id):

    user_id = int(get_jwt_identity())

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    drive = db.session.get(Drive, drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    if drive.status != "Approved":
        return jsonify({"message": "Drive not available for application"}), 400

    if drive.application_deadline and drive.application_deadline < date.today():
        return jsonify({"message": "Application deadline passed"}), 400

    existing = Placement.query.filter_by(student_id=student.id).first()
    if existing:
        return jsonify({"message": "Already placed, cannot apply"}), 400
    

    placed = Application.query.filter_by(
        student_id=student.id,
        status="Placed"
    ).first()

    if placed:
        return jsonify({"message": "Already placed. Cannot apply"}), 400

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


@student_bp.route("/student/upload_resume", methods=["POST"])
@jwt_required()
def upload_resume():

    user_id = int(get_jwt_identity())
    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    if "file" not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "Empty file"}), 400

    original_name = file.filename
    filename = f"{student.id}_{original_name}"

    upload_folder = os.path.join(os.getcwd(), "uploads")

    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filepath = os.path.join(upload_folder, filename)

    file.save(filepath)

    student.resume = filename   
    db.session.commit()
    return jsonify({"message": "Resume uploaded successfully"})


@student_bp.route("/student/my_applications", methods=["GET"])
@jwt_required()
def my_applications():

    user_id = int(get_jwt_identity())

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    applications = Application.query.filter_by(student_id=student.id).all()

    result = []

    for a in applications:

        drive = db.session.get(Drive, a.drive_id)

        if drive:
            company = db.session.get(Company, drive.company_id)

            company_name = ""
            if company:
                company_name = company.company_name

            result.append({
                "application_id": a.id,
                "company_name": company_name,
                "job_title": drive.job_title,
                "status": a.status,
                "applied_on": str(a.application_date),
                "interview_date": str(a.interview_date) if a.interview_date else ""
            })

    return jsonify(result)