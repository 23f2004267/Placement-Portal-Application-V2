from . import db
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username =db.Column(db.String(100),unique=True, nullable=False)
    password=db.Column(db.String(100),nullable=False)
    role=db.Column(db.String(15),nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    
