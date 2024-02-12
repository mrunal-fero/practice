import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_task.settings")
app = Celery("demo_task")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()