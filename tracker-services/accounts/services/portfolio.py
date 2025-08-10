from decimal import Decimal
from django.utils import timezone
from accounts.models import Account, Holdings, Lots, Security, Transactions
from securities.models import Security
from django.db import connection


class PortfolioService:
    @staticmethod
    def calculate_holding_pnl(holding):
        pass

    @staticmethod
    def get_current_market_price(symbol):
        with connection.cursor() as cursor:
            latest_price = cursor.execute("""
            UPDATE user_account AS acc
            SET net_worth = sub.total + COALESCE(acc.cash_balance, 0), total_market_value = sub.total
            FROM (
                SELECT account_id, SUM(quantity * current_price) AS total
                FROM holdings
                GROUP BY account_id
            ) AS sub
            WHERE acc.id = sub.account_id;
        """)


