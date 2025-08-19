import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, PriceHistory, TechnicalIndicators
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
                ORDER BY s.symbol, ph.date ASC
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
        calculated_data = self.calculate_indicators()

    def calculate_indicators(self):
        rows = []
        for symbol in self.symbols:
            symbol_df = self.data[self.data['symbol'] == symbol]
            symbol_df = symbol_df.sort_values('date')
            print(symbol_df.head())
            sma_20 = self.calc_sma(symbol_df, 20)
            sma_50 = self.calc_sma(symbol_df, 50)
            sma_200 = self.calc_sma(symbol_df, 200)
            ema_12 = self.calc_ema(symbol_df, 12)
            ema_26 = self.calc_ema(symbol_df, 26)
            rsi_14 = self.calc_rsi(symbol_df, 14)
            macd_line = self.calc_macd_line(ema_12, ema_26)
            bb_data = self.calc_bb(symbol_df, 20, 2)
            support_level = self.calc_support(symbol_df, 20)
            resistance_level = self.calc_resistance(symbol_df, 20)

            rows.append({
                'symbol': symbol,
                'date': self.current_date,
                'sma_20': sma_20,
                'sma_50': sma_50,
                'sma_200': sma_200,
                'ema_12': ema_12,
                'ema_26': ema_26,
                'rsi_14': rsi_14,
                'macd_line': macd_line,
                'macd_signal': 0, #TODO: need more data
                'bb_upper': bb_data['bb_upper'].iloc[-1],
                'bb_middle': bb_data['bb_middle'].iloc[-1],
                'bb_lower': bb_data['bb_lower'].iloc[-1],
                'support_level': support_level,
                'resistance_level': resistance_level,
            })
        print(rows)
        return rows

    def calc_sma(self, data, days):
        return data['close_price'].rolling(window=days, min_periods=1).mean().iloc[-1]

    def calc_ema(self, data, days):
        alpha = 2 / (days + 1)
        return data['close_price'].ewm(alpha=alpha, adjust=False, min_periods=1).mean().iloc[-1]

    def calc_rsi(self, data, days):
        close_prices = data['close_price']
        delta = close_prices.diff()
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)

        alpha = 1 / days
        avg_gains = gains.ewm(alpha=alpha, adjust=False, min_periods=days).mean()
        avg_losses = losses.ewm(alpha=alpha, adjust=False, min_periods=days).mean()

        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))

        return rsi.iloc[-1]

    def calc_macd_line(self, ema12, ema26):
        return ema12 - ema26

    def calc_bb(self, data, days, std=2):
        close_prices = data['close_price']
        bb_middle = close_prices.rolling(window=days).mean()

        rolling_std = close_prices.rolling(window=days).std()

        bb_upper = bb_middle + (std * rolling_std)
        bb_lower = bb_middle - (std * rolling_std)

        return {
            'bb_middle': bb_middle,
            'bb_upper': bb_upper,
            'bb_lower': bb_lower
        }

    def calc_support(self, data, days):
        recent_lows = data['low_price'].tail(days)
        return recent_lows.min()

    def calc_resistance(self, data, days):
        recent_highs = data['high_price'].tail(days)
        return recent_highs.max()