from flask import Flask
from config import Config
from models import db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
from flask import send_from_directory

from extensions import cache

from models.user import User
from models.student import Student
from models.company import Company
from models.drive import Drive
from models.application import Application
from models.placement import Placement

from routes.auth_routes import auth_bp
from routes.student_routes import student_bp
from routes.company_routes import company_bp
from routes.admin_routes import admin_bp


app = Flask(__name__)

CORS(app)

app.config.from_object(Config)
app.config["broker_url"] = Config.broker_url
app.config["result_backend"] = Config.result_backend

print("DATABASE URI:", app.config["SQLALCHEMY_DATABASE_URI"])
print("INSTANCE PATH:", app.instance_path)

db_uri = app.config["SQLALCHEMY_DATABASE_URI"]

if db_uri and db_uri.startswith("sqlite:///"):
    db_path = db_uri.replace("sqlite:///", "")
    print("ACTIVE SQLITE DB FILE:", os.path.abspath(db_path))
else:
    print("ACTIVE DATABASE IS NOT SQLITE")


db.init_app(app)

jwt = JWTManager(app)

cache.init_app(app)


app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)
app.register_blueprint(admin_bp)

from flask_jwt_extended import jwt_required

@app.route("/exports/<filename>")
def get_export_file(filename):

    export_folder = os.path.join(os.getcwd(), "exports")

    return send_from_directory(export_folder, filename)


@app.route("/uploads/<filename>")
def get_file(filename):

    upload_folder = os.path.join(os.getcwd(), "uploads")

    return send_from_directory(upload_folder, filename)


@app.route("/")
def home():
    return "Placement Portal Backend Run check"


from sqlalchemy.exc import OperationalError

with app.app_context():

    try:
        db.create_all()
        print("Tables created successfully")
    except Exception as e:
        print("DB create error:", e)

    try:
        admin = User.query.filter_by(role="admin").first()

        if not admin:
            admin = User(
                username="Vimlendu",
                password=generate_password_hash("Vimlendu@2001"),
                role="admin"
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin created")

    except Exception as e:
        print("Admin creation skipped:", e)

if __name__ == "__main__":
    app.run(debug=True)