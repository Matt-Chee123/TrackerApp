import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, MarketSnapshot, RiskMetrics
import pandas as pd
import math
from django.db import connection



class RiskMetricsService:

    def __init__(self):
        self.symbols = self.get_all_symbols()
        self.lookbackArray = [30]
        self.current_date = timezone.now().date()
        self.cutoff_date = self.current_date - timedelta(days=int(252 * 1.4))
        self.data_returns = self.get_1d_returns()

    def get_all_symbols(self):
        symbols = list(Security.objects.values_list('symbol', flat=True))
        return symbols

    def get_1d_returns(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    s.symbol,
                    ph.date,
                    ph.return_1d
                FROM securities_pricehistory ph
                INNER JOIN security s ON ph.security_id = s.symbol
                WHERE ph.date >= %s AND ph.return_1d IS NOT NULL
                ORDER BY s.symbol, ph.date ASC
            """, [self.cutoff_date])

            rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=[
            'symbol', 'date', 'return_1d'
        ])

        df['date'] = pd.to_datetime(df['date'])

        return df

    def update_risk_model(self):
        self.calculate_risk_indicators()
        return

    def calculate_risk_indicators(self):
        data = []
        for symbol in self.symbols:
            symbol_df = self.data_returns[self.data_returns['symbol'] == symbol]
            for lookback in self.lookbackArray:
                spliced_df = symbol_df.tail(lookback)
                print(symbol)
                print(lookback)
                print(symbol_df.head())
                print(symbol_df.shape())
                print(spliced_df)
                print(spliced_df.shape)
                # volatility_annualized = self.get_volatility_annualized(symbol_df, lookback)


                data.append({
                    'security': symbol,
                    'calculation_date': self.current_date,
                    'lookback_period': lookback,
                    'volatility_annualized': 0,
                    'sharpe_ratio': 0,
                    'sortino_ratio': 0,
                    'max_drawdown': 0,
                    'var_95': 0,
                    'var_99': 0,
                    'beta': 0,
                    'alpha': 0,
                    'correlation_market': 0,
                    'total_return': 0,
                    'annualized_return': 0,
                })

        return

    def get_volatility_annualized(self, data, lookback):

        return 0