import os
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Django_scrping_task_with_celery.settings')

app = Celery(
    'Django_scrping_task_with_celery',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
