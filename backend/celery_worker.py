from celery import Celery
from app import app
print("CELERY BROKER:", app.config.get("broker_url"))
print("CELERY BACKEND:", app.config.get("result_backend"))


celery = Celery(
    app.import_name,
    broker=app.config["broker_url"],
    backend=app.config["result_backend"]
)

celery.conf.update(app.config)
from celery.schedules import crontab

celery.conf.beat_schedule = {
    "send-interview-reminders-every-day": {
        "task": "tasks.reminder_tasks.send_interview_reminders",
        "schedule": crontab(hour=9, minute=0),
    }
}


class ContextTask(celery.Task):

    def __call__(self, *args, **kwargs):

        with app.app_context():

            return self.run(*args, **kwargs)


celery.Task = ContextTask


import tasks.reminder_tasks
import tasks.export_tasks
import tasks.report_tasks

