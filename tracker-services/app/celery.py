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
        'schedule': crontab(minute='*/30')
    },
    'update-securities-regular': {
        'task': 'securities.tasks.update_securities_prices',
        'schedule': crontab(minute='*/15')
    },
    'update-price-history-daily': {
        'task': 'securities.tasks.update_price_history_data',
        'schedule': crontab(minute='*')#crontab(hour='21',minute='0')
    },
    'update-account-total-daily': {
        'task': 'accounts.tasks.update_portfolio_metrics',
        'schedule': crontab(hour='*/3', minute='0')
    },
    'update-snapshot-data': {
        'task': 'securities.tasks.update_snapshot_data',
        'schedule': crontab(minute='*/5')
    }
}

app.conf.timezone = 'UTC'