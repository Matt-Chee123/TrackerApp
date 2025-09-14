from securities.models import Security
from django.db import connection, transaction
from django.utils import timezone


class PortfolioService:
    def __init(self):
        return

    def update_security_price(self, symbol, price):
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE security 
                    SET last_price = %s, updated_at = NOW() WHERE symbol = %s;
            """, [price, symbol])
            return True

    def get_security_price(self, symbol):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT last_price, updated_at FROM 
                security WHERE symbol = %s;
            """, [symbol])
            security_price = cursor.fetchone()
            #TODO: date check to see if security data out of wack

            return security_price


    def get_mock_prices(self):
        return {
            'AAPL': 190.25,
            'MSFT': 335.40,
            'GOOG': 125.60,
        }