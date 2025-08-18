import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, PriceHistory
import pandas as pd
import math
from django.db import connection


class TechnicalIndicatorService:

    def __init__(self):
        self.symbols = self.get_all_symbols()
        self.lookback_days = 252
        self.current_date = timezone.now().date()
        self.cutoff_date = self.current_date - timedelta(days=int(self.lookback_days * 1.4))
        self.data = self.get_historical_data()
        self.indicator_df = self.setup_indicator_df()

    def get_all_symbols(self):
        symbols = list(Security.objects.values_list('symbol', flat=True))
        return symbols

    def get_historical_data(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    s.symbol,
                    ph.date,
                    ph.open_price,
                    ph.high_price,
                    ph.low_price, 
                    ph.close_price,
                    ph.volume
                FROM securities_pricehistory ph
                INNER JOIN security s ON ph.security_id = s.symbol
                WHERE ph.date >= %s
                ORDER BY s.symbol, ph.date DESC
            """, [self.cutoff_date])

            rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=[
            'symbol', 'date', 'open_price', 'high_price',
            'low_price', 'close_price', 'volume'
        ])

        df['date'] = pd.to_datetime(df['date'])

        print(df.head())
        return df

    def setup_indicator_df(self):
        data = []
        columns = ['symbol', 'date', 'sma_20', 'sma_50', 'sma_200', 'ema_12', 'ema_26', 'rsi_14', 'macd_line', 'macd_signal', 'bb_upper', 'bb_middle', 'bb_lower', 'support_level', 'resistance_level']

        for symbol in self.symbols:
            data.append({'symbol': symbol, 'date': self.current_date})

        df = pd.DataFrame(data, columns=columns)
        print(df.head())
        return df