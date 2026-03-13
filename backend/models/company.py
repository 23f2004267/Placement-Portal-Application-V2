from . import db
class Company(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    company_name=db.Column(db.String(50),nullable=False)
    industry=db.Column(db.String(50))
    location=db.Column(db.String(200))
    website=db.Column(db.String(100))
    hr_contact=db.Column(db.String(50))
    approval_status=db.Column(db.String(20),default="Pending")

