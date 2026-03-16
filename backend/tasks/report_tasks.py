from celery_worker import celery

from models.application import Application
from models.drive import Drive
from models import db


@celery.task
def generate_monthly_report():

    total_drives = Drive.query.count()

    total_applications = Application.query.count()

    selected_students = Application.query.filter_by(
        status="Selected"
    ).count()

    filename = "placement_report.txt"

    with open(filename, "w") as file:

        file.write("Monthly Placement Report\n\n")

        file.write(f"Total Drives Conducted: {total_drives}\n")

        file.write(f"Total Applications: {total_applications}\n")

        file.write(f"Students Selected: {selected_students}\n")

    return "Monthly report generated"