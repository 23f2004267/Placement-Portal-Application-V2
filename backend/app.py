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

CORS(app, supports_credentials=True)

db.init_app(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)

jwt = JWTManager(app)

cache.init_app(app)


app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)
app.register_blueprint(admin_bp)

from flask import send_from_directory

@app.route("/uploads/<filename>")
def get_file(filename):
    upload_folder = os.path.join(os.getcwd(), "uploads")
    return send_from_directory(upload_folder, filename)

@app.route("/exports/<filename>")
def get_export_file(filename):
    export_folder = os.path.join(os.getcwd(), "exports")
    return send_from_directory(export_folder, filename)


@app.route("/")
def home():
    return "Placement Portal Backend Run check"


from sqlalchemy.exc import OperationalError

with app.app_context():

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

    except OperationalError:
        print("Tables not ready yet (migration pending)")


if __name__ == "__main__":
    app.run(debug=True)