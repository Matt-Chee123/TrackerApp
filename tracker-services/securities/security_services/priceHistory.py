import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, PriceHistory
import pandas as pd
from datetime import date, timedelta
from django.db import connection

class PriceHistoryService:
 #TODO: check this is working as only 4 symbols being updates
    def __init__(self):
        self.symbols = self.get_all_symbols()
        self.current_date = date.today()
        self.data = self.get_security_data()

    def update_price_history(self):

        for symbol in self.symbols:
            info = self.data[symbol]
            day_return = self.get_1d_return(info, symbol)
            price_history, created = PriceHistory.objects.update_or_create(
                security_id=symbol,
                date=self.current_date,
                defaults={
                    'open_price': info["Open"].iloc[0],
                    'high_price': info["High"].iloc[0],
                    'low_price': info["Low"].iloc[0],
                    'close_price': info["Close"].iloc[0],
                    'adjusted_close': info["Adj Close"].iloc[0],
                    'volume': info["Volume"].iloc[0],
                    'return_1d': day_return
                }
            )
        self.update_security_average_volume()
        pass

    def update_security_average_volume(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH volume_data AS (
                    SELECT 
                        security_id,
                        AVG(volume) AS average_volume 
                    FROM securities_pricehistory 
                    WHERE date >= CURRENT_DATE - INTERVAL '30 days' 
                    GROUP BY security_id
                )
                UPDATE security SET average_volume = vd.average_volume
                FROM volume_data AS vd
                WHERE symbol = vd.security_id
                 """)
            return

    def get_1d_return(self, data, symbol):
        yesterday = self.current_date - timedelta(days=1)

        yesterday_record = PriceHistory.objects.filter(
            security_id=symbol,
            date__lt=self.current_date
        ).order_by('-date').first()

        yesterday_close = float(yesterday_record.close_price)
        today_close = float(data['Close'])
        result = (today_close - yesterday_close) / yesterday_close

        print("xxxxxxxxxxxxxx")
        print(symbol)
        print(yesterday_close)
        print(today_close)
        print(result)
        return float(result)

    def get_security_data(self):
        if not self.symbols:
            print("No symbols found.")
            return

        tomorrow = self.current_date + timedelta(days=1)

        df = yf.download(
            tickers=" ".join(self.symbols),
            start=self.current_date,
            end=tomorrow,
            interval="1d",
            group_by="ticker",
            auto_adjust=False,
            threads=True
        )

        return df

    def get_all_symbols(self):
        symbols = list(Security.objects.values_list('symbol', flat=True))
        return symbols