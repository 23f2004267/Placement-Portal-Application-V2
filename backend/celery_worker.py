from celery import Celery
from app import app


celery = Celery(
    app.import_name,
    broker=app.config["CELERY_BROKER_URL"],
    backend=app.config["CELERY_RESULT_BACKEND"]
)

celery.conf.update(app.config)


class ContextTask(celery.Task):

    def __call__(self, *args, **kwargs):

        with app.app_context():

            return self.run(*args, **kwargs)


celery.Task = ContextTask


import tasks.reminder_tasks
import tasks.export_tasks
import tasks.report_tasks