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
from .security_services.technicalIndicators import TechnicalIndicatorService

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
    return service.update_snapshot_data()

@shared_task
def update_securities_prices():
    service = SecurityService()
    return service.update_security_prices()

@shared_task
def update_technical_indicators():
    service = TechnicalIndicatorService()
    service.update_technical_indicators_df()
    return

