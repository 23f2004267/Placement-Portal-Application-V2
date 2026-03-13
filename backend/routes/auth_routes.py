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

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    new_user = User(
        username=username,
        password=generate_password_hash(password),
        role="student"
    )

    db.session.add(new_user)
    db.session.commit()

    student_profile = Student(
        user_id=new_user.id,
        name=name,
        email=email
    )

    db.session.add(student_profile)
    db.session.commit()

    return jsonify({"message": "Student registered successfully"})


@auth_bp.route("/register/company", methods=["POST"])
def register_company():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    company_name = data.get("company_name")
    website = data.get("website")

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    new_user = User(
        username=username,
        password=generate_password_hash(password),
        role="company"
    )

    db.session.add(new_user)
    db.session.commit()

    company_profile = Company(
        user_id=new_user.id,
        company_name=company_name,
        website=website
    )

    db.session.add(company_profile)
    db.session.commit()

    return jsonify({"message": "Company registered. Waiting for admin approval."})



@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"message": "User not found"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Incorrect password"}), 401

    token = create_access_token(identity=user.id)

    return jsonify({
        "token": token,
        "role": user.role
    })