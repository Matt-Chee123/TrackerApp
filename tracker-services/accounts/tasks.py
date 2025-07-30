from celery import shared_task
from .utils import (
    bulk_update_accounts_total_value
)

@shared_task
def update_all_net_worths(symbol):
    return bulk_update_accounts_total_value(symbol)