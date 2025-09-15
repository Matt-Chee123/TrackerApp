import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, MarketSnapshot
import pandas as pd
import math


class MarketSnapshotService:

    def __init__(self):
        self.symbols = self.get_all_symbols()
        self.market_data = self.retrieve_market_data(self.symbols)

    def get_all_symbols(self):
        symbols = list(Security.objects.values_list('symbol', flat=True))
        return symbols

    def retrieve_market_data(self,symbols):
        if not self.symbols:
            print("No symbols found.")
            return

        symbols_str = ' '.join(symbols)

        df = self.create_snapshot_df()
        tickers = yf.Tickers(symbols_str)

        for symbol in symbols:
            ticker = tickers.tickers[symbol]
            info = ticker.info

            row = {
                'security': symbol,
                'current_price': info.get('currentPrice'),
                'bid_price': info.get('bid'),
                'ask_price': info.get('ask'),
                'bid_size': info.get('bidSize'),
                'ask_size': info.get('askSize'),
                'open_price': info.get('open'),
                'high_price': info.get('dayHigh'),
                'low_price': info.get('dayLow'),
                'volume': info.get('volume'),
                'change_amount': 0, #TODO
                'change_percent': 0, #TODO
                'market_timestamp': timezone.now(),
                'previous_close': info.get('previousClose'),
            }

            df.loc[len(df)] = row

        return df

    def calculate_change_amount(self, current_price, previous_close):
        change_amount = current_price - previous_close
        change_perc = change_amount / previous_close * 100
        return change_amount, change_perc

    #TODO : change this to be daily
    def calculate_avg_volume(self):
        hist = yf.download(self.symbols, period="30d", group_by='ticker', threads=True)
        volume_data = {}
        for symbol in self.symbols:
            symbol_data = hist[symbol]['Volume']
            volume_data[symbol] = {
                'avg_10d': int(symbol_data.tail(10).mean()),
                'avg_30d': int(symbol_data.mean())
            }
        return volume_data

    def create_snapshot_df(self):
        columns = [
            'security', 'current_price', 'bid_price', 'ask_price',
            'bid_size', 'ask_size', 'open_price', 'high_price',
            'low_price', 'volume', 'change_amount', 'change_percent',
            'market_timestamp', 'previous_close'
        ]
        return pd.DataFrame(columns=columns)

    def update_snapshot_data(self):
        if self.market_data.empty:
            print("No market data to update.")
            return

        avg_volumes = self.calculate_avg_volume()

        for _, row in self.market_data.iterrows():
            symbol = row['security']
            volume_data = avg_volumes[symbol]
            if math.isnan(row['current_price']):
                print("last price doesn't exist")
                row['current_price'] = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]

            row['change_amount'], row['change_percent'] = self.calculate_change_amount(row['current_price'], row['previous_close'])

            try:
                security_obj = Security.objects.get(symbol=symbol)
            except Security.DoesNotExist:
                print(f"Security {symbol} not found in DB, skipping.")
                continue

            def to_decimal(val):
                return Decimal(str(val)) if val is not None and not pd.isna(val) else None

            MarketSnapshot.objects.update_or_create(
                security=security_obj,
                defaults={
                    'current_price': to_decimal(row['current_price']),
                    'bid_price': to_decimal(row['bid_price']),
                    'ask_price': to_decimal(row['ask_price']),
                    'bid_size': row['bid_size'],
                    'ask_size': row['ask_size'],
                    'open_price': to_decimal(row['open_price']),
                    'high_price': to_decimal(row['high_price']),
                    'low_price': to_decimal(row['low_price']),
                    'previous_close': to_decimal(row['previous_close']),
                    'volume': int(row['volume']) if row['volume'] is not None else 0,
                    'change_amount': to_decimal(row['change_amount']),
                    'change_percent': to_decimal(row['change_percent']),
                    'market_timestamp': row['market_timestamp'],
                    'avg_volume_10d': volume_data['avg_10d'],
                    'avg_volume_30d': volume_data['avg_30d']
                }
            )
        return