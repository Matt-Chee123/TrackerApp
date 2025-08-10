from celery import shared_task
from .utils import (
    bulk_update_accounts_total_value
)
from .services.portfolio import PortfolioService


@shared_task
def update_all_net_worths():
    return PortfolioService.update_portfolio_stats()
