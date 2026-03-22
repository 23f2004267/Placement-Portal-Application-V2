from . import db
class Drive(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    company_id=db.Column(db.Integer, db.ForeignKey('company.id'))
    job_title=db.Column(db.String(50))
    job_description=db.Column(db.Text)
    eligibility_branch=db.Column(db.String(50))
    eligibility_cgpa=db.Column(db.Float)
    salary=db.Column(db.Integer)
    application_deadline=db.Column(db.Date)
    status=db.Column(db.String(20),default="Pending")

    company = db.relationship('Company', backref='drives')