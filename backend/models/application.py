from . import db


class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'))

    application_date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    status = db.Column(
        db.String(50),
        default="Applied"
    )

    interview_date = db.Column(
        db.DateTime,
        nullable=True
    )