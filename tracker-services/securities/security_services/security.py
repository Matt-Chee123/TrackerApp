import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, PriceHistory
import pandas as pd
from django.db import connection


class SecurityService:

    def __init__(self):
        self.symbols = self.get_all_symbols()


    def get_all_symbols(self):
        print("Retrieving all symbols")
        symbols = list(Security.objects.values_list('symbol', flat=True))
        print("Retrieved these symbols: ",symbols)
        return symbols

    def update_security_prices(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                    WITH snapshot_data AS (
                        SELECT security_id, last_price 
                        FROM securities_marketsnapshot
                    )
                    UPDATE security
                        SET last_price = sd.last_price,
                        price_updated_at = NOW(),
                        market_cap = sd.last_price * shares_outstanding
                    FROM snapshot_data AS sd
                    WHERE symbol = sd.security_id
                    """)
            return
