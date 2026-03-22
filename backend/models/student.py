from . import db
class Student(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'), unique=True)
    name=db.Column(db.String(25), nullable=False)
    email =db.Column(db.String(30), unique=True)
    phone=db.Column(db.String(20))
    branch=db.Column(db.String(20))
    cgpa=db.Column(db.Float)
    graduation_year =db.Column(db.Integer)
    skills=db.Column(db.Text)
    resume=db.Column(db.String(100))

    user = db.relationship('User', backref='student', uselist=False)