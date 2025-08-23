import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, MarketSnapshot, RiskMetrics
import pandas as pd
import math
from django.db import connection
import numpy as np




class RiskMetricsService:

    def __init__(self):
        self.symbols = self.get_all_symbols()
        self.lookbackArray = [30]
        self.current_date = timezone.now().date()
        self.cutoff_date = self.current_date - timedelta(days=int(252 * 1.4))
        self.data_returns = self.get_1d_returns()
        self.risk_free_rate = self.get_risk_free()

    def get_all_symbols(self):
        symbols = list(Security.objects.values_list('symbol', flat=True))
        return symbols

    def get_risk_free(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT last_price FROM security WHERE symbol = '^TNX';
            """)

            row = cursor.fetchone()

        if row and row[0] is not None:
            return float(row[0]) / 100
        else:
            return 0.04

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
        grouped_data = self.data_returns.groupby('symbol')

        for symbol, symbol_df in grouped_data:
            for lookback in self.lookbackArray:
                spliced_df = symbol_df.tail(lookback)
                returns = data['return_1d'].astype('float')

                print(symbol)
                print(spliced_df.head())

                total_return = self.calc_total_return(spliced_df)
                annualized_return = self.calc_annualized_return(total_return, len(returns))
                volatility_annualized = self.calc_volatility_annualized(returns)


                print(annualized_return)
                print(volatility_annualized)

                data.append({
                    'security': symbol,
                    'calculation_date': self.current_date,
                    'lookback_period': lookback,
                    'total_return': total_return,
                    'annualized_return': annualized_return,
                    'volatility_annualized': volatility_annualized,
                    'max_drawdown': 0,
                    'var_95': 0,
                    'var_99': 0,
                    'beta': 0,
                    'correlation_market': 0,
                    'sharpe_ratio': 0,
                    'sortino_ratio': 0,
                    'alpha': 0,
                })

        return

    def calc_total_return(self, returns):
        sum = np.prod(returns + 1) - 1
        return sum

    def calc_annualized_return(self, total_return, lookback_period):
        sum = (1 + total_return) ** (252 / lookback_period) - 1
        return sum

    def calc_volatility_annualized(self, returns):
        daily_std = returns.std()
        annualized_volatility = daily_std * math.sqrt(252)
        return annualized_volatility

    def calc_sharpe_ratio(self, data):

        return