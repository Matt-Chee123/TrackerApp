from celery import shared_task
from .utils import (
    update_stock_price,
    get_dividend_and_split_data,
    bulk_update_securities,
    bulk_update_dividends_and_splits,
)

@shared_task
def update_single_security(symbol):
    return update_stock_price(symbol)

@shared_task
def update_dividends_splits(symbol):
    return get_dividend_and_split_data(symbol)

@shared_task
def update_all_securities(symbols):
    return bulk_update_securities(symbols)

@shared_task
def update_all_dividends_and_splits(symbols):
    return bulk_update_dividends_and_splits(symbols)
