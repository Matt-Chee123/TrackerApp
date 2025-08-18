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

        return df

    def setup_indicator_df(self):
        data = []
        columns = ['symbol', 'date', 'sma_20', 'sma_50', 'sma_200', 'ema_12', 'ema_26', 'rsi_14', 'macd_line', 'macd_signal', 'bb_upper', 'bb_middle', 'bb_lower', 'support_level', 'resistance_level']

        for symbol in self.symbols:
            data.append({'symbol': symbol, 'date': self.current_date})

        df = pd.DataFrame(data, columns=columns)
        return df

    def update_technical_indicators_df(self):
        rows = []
        for symbol in self.symbols:
            symbol_df = self.data[self.data['symbol'] == symbol]
            sma_20 = self.calc_sma(symbol_df, 20)
            sma_50 = self.calc_sma(symbol_df, 50)
            sma_200 = self.calc_sma(symbol_df, 200)

            rows.append({
                'symbol': symbol,
                'date': self.current_date,
                'sma_20': sma_20,
                'sma_50': sma_50,
                'sma_200': sma_200,
                'ema_12': 0,
                'ema_26': 0,
                'rsi_14': 0,
                'macd_line': 0,
                'macd_signal': 0,
                'bb_upper': 0,
                'bb_middle': 0,
                'bb_lower': 0,
                'support_level': 0,
                'resistance_level': 0,
            })
        print(rows)
        return

    def calc_sma(self, data, days):
        return data['close_price'].rolling(window=days, min_periods=1).mean().iloc[-1]