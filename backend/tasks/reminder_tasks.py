from datetime import datetime, timedelta

from celery_worker import celery

from models.application import Application
from models.student import Student
from models.drive import Drive
from models import db


@celery.task
def send_interview_reminders():

    tomorrow = datetime.now() + timedelta(days=1)

    applications = Application.query.filter(
        Application.interview_date != None
    ).all()

    for app in applications:

        interview_time = app.interview_date

        if interview_time.date() == tomorrow.date():

            student = db.session.get(Student, app.student_id)
            drive = db.session.get(Drive, app.drive_id)

            message = (
                f"Reminder: {student.name}, "
                f"you have an interview for {drive.job_title} "
                f"on {interview_time}"
            )

            print(message)