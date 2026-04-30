from datetime import datetime, timedelta
from utils.email_service import send_email

from celery_worker import celery

from models.application import Application
from models.student import Student
from models.drive import Drive
from models import db


@celery.task
def send_interview_reminders():

    now = datetime.now()

    applications = Application.query.filter(
        Application.interview_date != None
    ).all()

    for app in applications:

        interview_time = app.interview_date

        if not interview_time:
            continue

        time_diff = interview_time - now
        minutes = time_diff.total_seconds() / 60

        student = db.session.get(Student, app.student_id)
        drive = db.session.get(Drive, app.drive_id)
        company_name = drive.company.company_name if drive else "Company"

        if 1430 < minutes < 1450 and not app.reminder_24_sent:
            send_email(
                student.email,
                "Reminder: Upcoming Interview",
                f"Dear {student.name}, your interview for {drive.job_title} at {company_name} is tomorrow at {interview_time}."
            )
            app.reminder_24_sent = True

        elif 230 < minutes < 250 and not app.reminder_4_sent:
            send_email(
                student.email,
                "Interview Reminder",
                f"Hi {student.name}, your interview for {drive.job_title} is in a few hours. Be prepared."
            )
            app.reminder_4_sent = True

        elif 20 < minutes < 40 and not app.reminder_30_sent:
            send_email(
                student.email,
                "Interview Starting Soon",
                f"Hi {student.name}, your interview starts in 30 minutes. Stay ready!"
            )
            app.reminder_30_sent = True

    db.session.commit()


def send_interview_email(student_email, student_name, job_title, interview_time, company_name):

    subject = f"Interview Scheduled – {company_name}"

    body = f"""
Dear {student_name},

We are pleased to inform you that your interview for the position of {job_title} at {company_name} has been successfully scheduled.

Interview Details:
Date & Time: {interview_time}

Please ensure you are prepared and available at the scheduled time.

We wish you the best of luck.

Regards,
{company_name}
"""

    send_email(student_email, subject, body)

    print("EMAIL SENT TO:", student_email)