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

    applications = Application.query.filter_by(student_id=student.id).all()

    return jsonify({
        "student_name": student.name,
        "phone": student.phone,
        "branch": student.branch,
        "cgpa": student.cgpa,
        "skills": student.skills,
        "resume": student.resume,
        "total_applications": len(applications)
    })


@student_bp.route("/student/drives", methods=["GET"])
@jwt_required()
def view_drives():

    user_id = int(get_jwt_identity())

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    drives = Drive.query.all()

    result = []

    for d in drives:
        company = db.session.get(Company, d.company_id)

        if company:
            application = Application.query.filter_by(
                student_id=student.id,
                drive_id=d.id
            ).first()

            result.append({
                "drive_id": d.id,
                "company_name": company.company_name,
                "job_title": d.job_title,
                "salary": d.salary,
                "drive_status": d.status,
                "application_status": application.status if application else "Not Applied"
            })

    return jsonify(result)


@student_bp.route("/student/search_drives", methods=["GET"])
@jwt_required()
def search_drives():

    user_id = int(get_jwt_identity())

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    title = request.args.get("title", "").strip()

    if not title:
        return jsonify([])

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

    application = None

    if user.role == "student":
        application = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive.id
        ).first()

    return jsonify({
        "drive_id": drive.id,
        "company_name": company_name,
        "job_title": drive.job_title,
        "job_description": drive.job_description,
        "salary": drive.salary,
        "status": drive.status,
        "application_status": application.status if application else "Not Applied",
        "interview_date": str(application.interview_date) if application and application.interview_date else ""
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

    if not student.resume:
        return jsonify({
            "message": "Please upload your resume before applying."
        }), 400

    if not student.phone:
        return jsonify({
            "message": "Please complete your profile."
        }), 400

    if not student.skills:
        return jsonify({
            "message": "Please complete your profile."
        }), 400

    if student.cgpa is None:
        return jsonify({
            "message": "Please complete your profile."
        }), 400

    if drive.status != "Approved":
        return jsonify({"message": "Drive not available for application"}), 400

    if drive.application_deadline and drive.application_deadline < date.today():
        return jsonify({"message": "Application deadline passed"}), 400


    existing_placement = Placement.query.filter_by(
        student_id=student.id
    ).first()

    if existing_placement:
        return jsonify({"message": "Already placed, cannot apply"}), 400


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

@student_bp.route("/student/upload_resume", methods=["POST", "OPTIONS"])
@jwt_required()
def upload_resume():

    if request.method == "OPTIONS":
        return jsonify({"message": "OK"}), 200

    user_id = int(get_jwt_identity())
    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    file = request.files.get("file")

    if not file:
        return jsonify({"message": "No file uploaded"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({
            "message": "Only PDF resumes are allowed."
        }), 400

    import os

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)

    filename = f"resume_{student.id}.pdf"
    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    student.resume = filename

    db.session.commit()

    return jsonify({
        "message": "Resume uploaded successfully",
        "resume": student.resume
    })

@student_bp.route("/student/update_profile", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = int(get_jwt_identity())
    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()

    phone = data.get("phone")
    branch = data.get("branch")
    cgpa = data.get("cgpa")
    skills = data.get("skills")

    if phone and (not phone.isdigit() or len(phone) != 10):
        return jsonify({"message": "Phone must be 10 digits"}), 400

    if cgpa is not None:
        try:
            cgpa = float(cgpa)
            if cgpa < 0 or cgpa > 10:
                return jsonify({"message": "CGPA must be between 0 and 10"}), 400
        except:
            return jsonify({"message": "Invalid CGPA"}), 400
    if not branch or not skills:
        return jsonify({"message": "Branch and Skills required"}), 400


    student.phone = phone
    student.branch = branch
    student.cgpa = cgpa
    student.skills = skills

    db.session.commit()

    return jsonify({"message": "Profile updated successfully"})


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

@student_bp.route("/student/export_applications", methods=["POST"])
@jwt_required()
def export_applications():

    user_id = int(get_jwt_identity())

    student = verify_student(user_id)

    if not student:
        return jsonify({"message": "Access denied"}), 403
    
    print("EXPORT API HIT")
    print("SENDING TASK TO CELERY")

    from tasks.export_tasks import export_student_applications
    export_student_applications.delay(student.id)
    return jsonify({"message": "Export started. File will be generated soon."})