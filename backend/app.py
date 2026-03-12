from flask import Flask
from config import Config
from models import db

from models.user import User
from models.student import Student
from models.company import Company
from models.drive import Drive
from models.application import Application
from models.placement import Placement

app=Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()
    
    admin=User.query.filter_by(role="admin").first()
    
    if not admin:
        admin = User(
            username="Vimlendu",
            password="Vimlendu@2003",
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
if __name__ == "__main__":
    app.run(debug=True)

    
