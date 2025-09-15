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
        symbols = list(Security.objects.values_list('symbol', flat=True))
        return symbols

    def update_security_prices(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                    WITH snapshot_data AS (
                        SELECT security_id, current_price 
                        FROM securities_marketsnapshot
                    )
                    UPDATE security
                        SET current_price = sd.current_price,
                        price_updated_at = NOW(),
                        market_cap = sd.current_price * shares_outstanding
                    FROM snapshot_data AS sd
                    WHERE symbol = sd.security_id
                    """)
            return
