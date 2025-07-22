import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')  # Note: underscores, not hyphens
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()