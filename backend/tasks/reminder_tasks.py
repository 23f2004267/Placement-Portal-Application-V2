from datetime import datetime, timedelta
from utils.email_service import send_email

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

        if interview_time and interview_time.date() == tomorrow.date():

            student = db.session.get(Student, app.student_id)
            drive = db.session.get(Drive, app.drive_id)

            message = (
                f"Reminder: {student.name}, "
                f"you have an interview for {drive.job_title} "
                f"on {interview_time}"
            )

            with open("notifications.log", "a") as f:
                f.write(message + "\n")

            print("NOTIFICATION SENT:", message)

            send_interview_email(
                student.email,
                student.name,
                drive.job_title,
                interview_time
            )


def send_interview_email(student_email, student_name, job_title, interview_time):

    subject = "Interview Scheduled"

    body = f"""
        Hello {student_name},

        Your interview has been scheduled.

        Job Title: {job_title}
        Interview Time: {interview_time}

        Best of luck!

        Placement Portal
        """

    send_email(student_email, subject, body)

    print("EMAIL SENT TO:", student_email)