from flask import Blueprint, request, jsonify
from models import db
from models.user import User
from models.student import Student
from models.company import Company

from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register/student", methods=["POST"])
def register_student():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    name = data.get("name")
    email = data.get("email")

    if not name:
        return jsonify({"message": "Name is required"}), 400

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:

        if existing_user.is_active:
            return jsonify({"message": "Username already exists"}), 400

        else:
            existing_user.password = generate_password_hash(password)
            existing_user.role = "student"
            existing_user.is_active = True

            student_profile = Student.query.filter_by(
                user_id=existing_user.id
            ).first()

            if student_profile:
                student_profile.name = name
                student_profile.email = email
            else:
                student_profile = Student(
                    user_id=existing_user.id,
                    name=name,
                    email=email
                )
                db.session.add(student_profile)

            db.session.commit()

            return jsonify({"message": "Student re-registered successfully"})

    try:
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            role="student"
        )

        db.session.add(new_user)

        db.session.flush()

        student_profile = Student(
            user_id=new_user.id,
            name=name,
            email=email
        )

        db.session.add(student_profile)

        db.session.commit()

        return jsonify({"message": "Student registered successfully"})

    except Exception:
        db.session.rollback()
        return jsonify({"message": "Registration failed"}), 500
    


@auth_bp.route("/register/company", methods=["POST"])
def register_company():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    company_name = data.get("company_name")
    website = data.get("website")

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    if not company_name:
        return jsonify({"message": "Company name is required"}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    existing_company = Company.query.filter_by(
        company_name=company_name
    ).first()

    if existing_company:
        return jsonify({"message": "Company already registered"}), 400

    try:
        new_user = User(
            username=username,
            password=generate_password_hash(password),
            role="company"
        )

        db.session.add(new_user)

        db.session.flush()

        company_profile = Company(
            user_id=new_user.id,
            company_name=company_name,
            website=website
        )

        db.session.add(company_profile)

        db.session.commit()

        return jsonify({"message": "Company registered. Waiting for admin approval."})

    except Exception:
        db.session.rollback()
        return jsonify({"message": "Company registration failed"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    if user.is_active is False:
        return jsonify({"message": "Your account is blacklisted"}), 403

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": token,
        "role": user.role,
        "user_id": user.id
    })