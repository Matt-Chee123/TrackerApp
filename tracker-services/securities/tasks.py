from celery import shared_task
from .utils import (
    update_stock_price,
    get_dividend_and_split_data,
    bulk_update_securities,
    bulk_update_dividends_and_splits,
)
from .security_services.security import SecurityService
from .security_services.priceHistory import PriceHistoryService
from .security_services.marketSnapshot import MarketSnapshotService

@shared_task
def update_all_securities():
    return

@shared_task
def update_price_history_data():
    service = PriceHistoryService()
    return service.update_price_history()

@shared_task
def update_snapshot_data():
    print("updating snapshot data")
    service = MarketSnapshotService()


