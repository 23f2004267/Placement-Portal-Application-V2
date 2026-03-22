from . import db
class Placement(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    student_id=db.Column(db.Integer, db.ForeignKey('student.id'), unique=True)
    company_id=db.Column(db.Integer, db.ForeignKey('company.id'))
    position=db.Column(db.String(50))
    salary=db.Column(db.Integer)
    joining_date=db.Column(db.Date)

    student = db.relationship('Student', backref='placement')
    company = db.relationship('Company', backref='placements')