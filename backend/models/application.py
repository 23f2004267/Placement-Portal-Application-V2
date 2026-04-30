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
    reminder_24_sent = db.Column(db.Boolean, default=False)
    reminder_4_sent = db.Column(db.Boolean, default=False)
    reminder_30_sent = db.Column(db.Boolean, default=False)
    
    interview_date = db.Column(
        db.DateTime,
        nullable=True
    )

    __table_args__ = (
        db.UniqueConstraint('student_id', 'drive_id', name='unique_application'),
    )

    student = db.relationship('Student', backref='applications')
    drive = db.relationship('Drive', backref='applications')