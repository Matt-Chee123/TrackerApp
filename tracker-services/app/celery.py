import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')  # Note: underscores, not hyphens
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-securities-daily': {
        'task': 'securities.tasks.update_all_securities',
        'schedule': crontab(hour='*/3', minute=0)
    },
    'update-account-total-daily': {
        'task': 'accounts.tasks.bulk_update_accounts_total_value',
        'schedule': crontab(hour='*/3', minute=0)
    },
}

app.conf.timezone = 'UTC'