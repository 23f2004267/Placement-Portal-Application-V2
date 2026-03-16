from flask import Flask
from config import Config
from models import db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager

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

db.init_app(app)

jwt = JWTManager(app)

cache.init_app(app)


app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def home():
    return "Placement Portal Backend Run check"


with app.app_context():

    db.create_all()

    admin = User.query.filter_by(role="admin").first()

    if not admin:

        admin = User(
            username="Vimlendu",
            password=generate_password_hash("Vimlendu@2001"),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)