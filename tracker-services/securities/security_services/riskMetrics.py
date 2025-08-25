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
        self.lookbackArray = [30,90]
        self.current_date = timezone.now().date()
        self.cutoff_date = self.current_date - timedelta(days=int(252 * 1.4))
        self.data_returns = self.get_1d_returns()
        self.risk_free_rate = self.get_risk_free()
        self.market_data = self.get_market_data()

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

    def get_market_data(self):
        with connection.cursor() as cursor:
            end_date = self.current_date
            start_date = self.current_date - timedelta(days=365)
            cursor.execute("""
                SELECT date, 
                    return_1d  
                    FROM securities_pricehistory                 
                WHERE 
                    security_id = '^GSPC'
                    AND date BETWEEN %s AND %s
                ORDER BY 
                    date ASC;
            """, [start_date, end_date])

            rows = cursor.fetchall()
            market_data = pd.DataFrame(rows, columns=['date','return_1d'])

            return market_data



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
                ORDER BY s.symbol, ph.date ASC;
            """, [self.cutoff_date])

            rows = cursor.fetchall()

        df = pd.DataFrame(rows, columns=[
            'symbol', 'date', 'return_1d'
        ])

        df['date'] = pd.to_datetime(df['date'])

        return df

    def update_risk_metrics(self):
        """Update or create risk metrics for each symbol and lookback period."""
        metrics_data = self.calculate_risk_indicators()  # First calculate the risk metrics

        for metric in metrics_data:
            # Use update_or_create to either update an existing record or create a new one
            risk_metrics_instance, created = RiskMetrics.objects.update_or_create(
                security=metric['security'],
                calculation_date=metric['calculation_date'],
                lookback_period=metric['lookback_period'],
                defaults={
                    'total_return': metric['total_return'],
                    'annualized_return': metric['annualized_return'],
                    'volatility_annualized': metric['volatility_annualized'],
                    'max_drawdown': metric['max_drawdown'],
                    'var_95': metric['var_95'],
                    'var_99': metric['var_99'],
                    'beta': metric['beta'],
                    'correlation_market': metric['correlation_market'],
                    'sharpe_ratio': metric['sharpe_ratio'],
                    'sortino_ratio': metric['sortino_ratio'],
                    'alpha': metric['alpha'],
                })

            if created:
                print(f"Created new record for {metric['security'].symbol} with {metric['lookback_period']} lookback.")
            else:
                print(
                    f"Updated existing record for {metric['security'].symbol} with {metric['lookback_period']} lookback.")

        return len(metrics_data)

    def calculate_risk_indicators(self):
        data = []
        grouped_data = self.data_returns.groupby('symbol')

        for symbol, symbol_df in grouped_data:
            for lookback in self.lookbackArray:
                spliced_df = symbol_df.tail(lookback)
                spliced_market_data = self.market_data.tail(lookback)
                returns = spliced_df['return_1d'].astype('float')
                market_returns = spliced_market_data['return_1d'].astype('float')


                total_return = self.calc_total_return(returns)
                annualized_return = self.calc_annualized_return(total_return, len(returns))
                volatility_annualized = self.calc_volatility_annualized(returns)
                max_drawdown = self.calc_max_drawdown(returns)
                var_95 = self.calc_var_hist_weighted(returns, 0.95, 0.94)
                var_99 = self.calc_var_hist_weighted(returns, 0.99, 0.94)
                beta = self.calc_beta(returns, market_returns)
                correlation_market = self.calculate_correlation_market(returns, market_returns)
                sharpe_ratio = self.calc_sharpe_ratio(returns)
                sortino_ratio = self.calc_sortino_ratio(returns)
                alpha = self.calc_alpha(returns, market_returns, beta)



                print(
                    f"{symbol}: Total return {total_return} Annual Return: {annualized_return * 100:.1f}%, Volatility: {volatility_annualized * 100:.1f}%")
                print("Value at risk 95: ", var_95, "var at risk 99:", var_99, "beta", beta, "sharpre ratio", sharpe_ratio, "sortino ratio", sortino_ratio)

                data.append({
                    'security': Security.objects.get(symbol=symbol),
                    'calculation_date': self.current_date,
                    'lookback_period': lookback,
                    'total_return': total_return,
                    'annualized_return': annualized_return,
                    'volatility_annualized': volatility_annualized,
                    'max_drawdown': max_drawdown,
                    'var_95': var_95,
                    'var_99': var_99,
                    'beta': beta,
                    'correlation_market': correlation_market,
                    'sharpe_ratio': sharpe_ratio,
                    'sortino_ratio': sortino_ratio,
                    'alpha': alpha,
                })

        return data


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

    def calc_max_drawdown(self, returns):
        r = pd.Series(returns, dtype="float64").dropna()
        wealth = (1.0 + r).cumprod()
        running_max = wealth.cummax()
        drawdown = wealth / running_max - 1.0
        mdd = drawdown.min()
        return float(-mdd)

    def calc_var_hist_weighted(self, returns, level, lam):
        r = pd.Series(returns, dtype="float64").dropna()
        if r.empty:
            return float("nan")
        n = len(r)
        w = np.power(lam, np.arange(n - 1, -1, -1))
        w /= w.sum()

        q = np.quantile(r, (1.0 - level), method="nearest")  # quick fallback
        sorter = np.argsort(r.values)
        r_sorted = r.values[sorter]
        w_sorted = w[sorter]
        cw = np.cumsum(w_sorted)
        idx = np.searchsorted(cw, (1.0 - level), side="right")
        q_w = r_sorted[min(idx, len(r_sorted) - 1)]
        return float(-q_w)

    def calc_beta(self, stock_data, market_data):
        covariance = np.cov(stock_data, market_data)[0][1]
        market_variance = np.var(market_data)

        return covariance / market_variance

    def calculate_correlation_market(self, stock_data, market_data):
        print("Original Stock Data:", stock_data.head())
        print("Original Market Data:", market_data.head())

        stock_data_reset = stock_data.reset_index(drop=True)
        market_data_reset = market_data.reset_index(drop=True)

        data = pd.concat([stock_data_reset, market_data_reset], axis=1, keys=['return_1d_x', 'return_1d_y'])

        correlation = data['return_1d_x'].corr(data['return_1d_y'])

        return correlation

    def calc_sharpe_ratio(self, returns):
        excess_returns = returns - self.risk_free_rate / 252
        sharpe_ratio = excess_returns.mean() / excess_returns.std() * math.sqrt(252)
        return sharpe_ratio

    def calc_sortino_ratio(self, returns):
        excess_returns = returns - self.risk_free_rate / 252

        downside_returns = excess_returns[excess_returns < 0]

        downside_deviation = downside_returns.std() if len(downside_returns) > 0 else np.nan

        if downside_deviation != 0:
            sortino_ratio = excess_returns.mean() / downside_deviation * math.sqrt(252)
        else:
            sortino_ratio = np.nan

        return sortino_ratio

    def calc_alpha(self, returns, market_returns, beta):
        market_return = market_returns.mean()
        expected_return = self.risk_free_rate / 252 + beta * (market_return - self.risk_free_rate / 252)

        actual_return = returns.mean()

        alpha = actual_return - expected_return

        alpha_annualized = alpha * 252
        return alpha_annualized