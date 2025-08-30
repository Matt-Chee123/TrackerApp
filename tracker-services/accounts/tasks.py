from celery import shared_task
from .utils import (
    bulk_update_accounts_total_value
)
from .services.portfolio import PortfolioService


@shared_task
def update_all_portfolio_stats():
    service = PortfolioService()
    return service.update_portfolio_stats()
