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
from datetime import timedelta

celery.conf.beat_schedule = {
    "check-reminders-every-minute": {
        "task": "tasks.reminder_tasks.send_interview_reminders",
        "schedule": timedelta(minutes=1),
    }
}


class ContextTask(celery.Task):

    def __call__(self, *args, **kwargs):

        with app.app_context():

            return self.run(*args, **kwargs)


celery.Task = ContextTask


from tasks import reminder_tasks
import tasks.export_tasks
import tasks.report_tasks
print("Loaded reminder tasks:", dir(reminder_tasks))

