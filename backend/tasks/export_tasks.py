import csv
import os
from datetime import datetime

from celery_worker import celery
from models.application import Application
from models.drive import Drive
from models.student import Student
from models.company import Company
from models import db


@celery.task
def export_student_applications(student_id):

    student = db.session.get(Student, student_id)

    applications = Application.query.filter_by(
        student_id=student_id
    ).all()

    export_folder = "exports"
    os.makedirs(export_folder, exist_ok=True)


    safe_name = student.name.replace(" ", "_")

    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = os.path.join(
        export_folder,
        f"{safe_name}_applications_{timestamp}.csv"
    )

    print("CURRENT DIRECTORY:", os.getcwd())
    print("FULL FILE PATH:", os.path.abspath(filename))

    with open(filename, "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Student Name",
            "Company",
            "Job Title",
            "Application Status"
        ])

        for app in applications:

            drive = db.session.get(Drive, app.drive_id)
            company = db.session.get(Company, drive.company_id) if drive else None

            writer.writerow([
                student.name if student else "",
                company.company_name if company else "",
                drive.job_title if drive else "",
                app.status
            ])

    return f"CSV Export Completed: {filename}"