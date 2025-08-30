import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')  # Note: underscores, not hyphens
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
#TODO change to correct timings
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
        'schedule': crontab(hour='*',minute='0')#crontab(hour='21',minute='0')
    },
    'update-account-holdings-daily': {
        'task': 'accounts.tasks.update_portfolio_metrics',
        'schedule':  crontab(minute='*')#crontab(hour='*/3', minute='0')
    },
    'update-account-total-daily': {
        'task': 'accounts.tasks.update_all_net_worths',
        'schedule': crontab(minute='*')  # crontab(hour='*/3', minute='0')
    },
    'update-snapshot-data': {
        'task': 'securities.tasks.update_snapshot_data',
        'schedule': crontab(minute='*/5')
    },
    'update-tech-indicators-daily': {
        'task': 'securities.tasks.update_technical_indicators',
        'schedule': crontab(hour='*',minute='5') #crontab(hour='21',minute='10')
    },
    'update-short-term-risk-data': {
        'task': 'securities.tasks.update_short_term_risk_metrics',
        'schedule': crontab(hour='*',minute='10') #crontab(hour='21',minute='15')
    }
}

app.conf.timezone = 'UTC'