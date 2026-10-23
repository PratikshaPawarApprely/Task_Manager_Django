from kombu import Queue
import os

from celery import Celery

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

app = Celery("config")

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

app.autodiscover_tasks()


app.conf.task_queues = (
    Queue("default"),
    Queue("notifications"),
    Queue("maintenance"),
)

app.conf.task_default_queue = "default"

app.conf.task_routes = {
    "tasks.tasks.process_task_notification": {
        "queue": "notifications",
    },
    "tasks.tasks.check_overdue_tasks": {
        "queue": "maintenance",
    },
}
