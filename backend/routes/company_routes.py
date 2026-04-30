from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User
from models.company import Company
from models.drive import Drive
from models.application import Application
from models.student import Student
from models.placement import Placement
from models import db


company_bp = Blueprint("company", __name__)


def verify_company(user_id):

    user = db.session.get(User, user_id)

    if user is None:
        return None

    if user.role != "company":
        return None

    if user.is_active == False:
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

    user_id = int(get_jwt_identity())

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

    user_id = int(get_jwt_identity())

    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()

    job_title = data.get("job_title")
    job_description = data.get("job_description")
    salary = data.get("salary")

    if not job_title or str(job_title).strip() == "":
        return jsonify({"message": "Job title is required"}), 400

    if not job_description or str(job_description).strip() == "":
        return jsonify({"message": "Job description is required"}), 400

    if salary is None or str(salary).strip() == "":
        return jsonify({"message": "Salary is required"}), 400

    try:
        salary = int(salary)
    except:
        return jsonify({"message": "Salary must be a number"}), 400

    if salary <= 0:
        return jsonify({"message": "Salary must be greater than 0"}), 400

    drive = Drive(
        company_id=company.id,
        job_title=job_title.strip(),
        job_description=job_description.strip(),
        salary=salary,
        status="Pending"
    )

    db.session.add(drive)
    db.session.commit()

    return jsonify({"message": "Placement drive created"})


@company_bp.route("/company/my_drives", methods=["GET"])
@jwt_required()
def my_drives():

    user_id = int(get_jwt_identity())

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

    user_id = int(get_jwt_identity())

    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    drive = db.session.get(Drive, drive_id)

    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    if drive.company_id != company.id:
        return jsonify({"message": "Unauthorized action"}), 403

    applications = Application.query.filter_by(drive_id=drive_id).all()

    result = []

    for app in applications:

        student = db.session.get(Student, app.student_id)

        result.append({
            "application_id": app.id,
            "student_name": student.name if student else "",
            "email": student.email if student else "",
            "phone": student.phone if student else "",
            "branch": student.branch if student else "",
            "cgpa": student.cgpa if student else "",
            "skills": student.skills if student else "",
            "status": app.status,
            "resume": student.resume if student else "",
            "interview_date": str(app.interview_date) if app.interview_date else ""
        })

    return jsonify(result)


@company_bp.route("/company/update_application/<int:app_id>", methods=["PUT"])
@jwt_required()
def update_application(app_id):

    user_id = int(get_jwt_identity())

    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    application = db.session.get(Application, app_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    drive = db.session.get(Drive, application.drive_id)

    if drive.company_id != company.id:
        return jsonify({"message": "Unauthorized action"}), 403

    data = request.get_json()

    new_status = data.get("status")
    interview_date = data.get("interview_date")

    valid_status = [
        "Applied",
        "Shortlisted",
        "Interview",
        "Offer",
        "Rejected",
        "Placed"
    ]

    if new_status not in valid_status:
        return jsonify({"message": "Invalid status"}), 400

    application.status = new_status

    if new_status == "Interview" and interview_date:
        from datetime import datetime
        try:
            interview_date = interview_date.replace("T", " ")
            application.interview_date = datetime.strptime(interview_date, "%Y-%m-%d %H:%M")
        except:
            return jsonify({"message": "Invalid datetime format"}), 400
        
        from tasks.reminder_tasks import send_interview_email

        student = db.session.get(Student, application.student_id)
        drive = db.session.get(Drive, application.drive_id)

        send_interview_email(
            student.email,
            student.name,
            drive.job_title,
            application.interview_date,
            drive.company.company_name
        )

    db.session.commit()

    return jsonify({"message": "Application status updated"})


@company_bp.route("/company/mark_placed/<int:app_id>", methods=["POST"])
@jwt_required()
def mark_placed(app_id):

    user_id = int(get_jwt_identity())

    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    application = db.session.get(Application, app_id)

    if not application:
        return jsonify({"message": "Application not found"}), 404

    drive = db.session.get(Drive, application.drive_id)

    if drive.company_id != company.id:
        return jsonify({"message": "Unauthorized action"}), 403

    existing = Placement.query.filter_by(student_id=application.student_id).first()
    if existing:
        return jsonify({"message": "Student already placed"}), 400

    if application.status == "Placed":
        return jsonify({"message": "Already placed"}), 400

    application.status = "Placed"

    placement = Placement(
        student_id=application.student_id,
        company_id=company.id,
        position=drive.job_title,
        salary=drive.salary
    )

    db.session.add(placement)
    db.session.commit()

    return jsonify({"message": "Student marked as placed"})

@company_bp.route("/company/complete_drive/<int:drive_id>", methods=["PUT"])
@jwt_required()
def complete_drive(drive_id):

    user_id = int(get_jwt_identity())
    company = verify_company(user_id)

    if not company:
        return jsonify({"message": "Access denied"}), 403

    drive = db.session.get(Drive, drive_id)

    if not drive or drive.company_id != company.id:
        return jsonify({"message": "Unauthorized"}), 403

    drive.status = "Completed"
    db.session.commit()

    return jsonify({"message": "Drive marked as completed"})