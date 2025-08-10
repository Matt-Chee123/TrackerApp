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
    def get_current_market_price():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM security WHERE symbol = %s
            """, ['AAPL'])
            row = cursor.fetchone()
        return row[0] if row else None


