import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, MarketSnapshot
import pandas as pd
from datetime import date, timedelta

class MarketSnapshotService:

    def __init__(self):
        self.symbols = self.get_all_symbols()
        self.market_data = self.retrieve_market_data(self.symbols)

    def get_all_symbols(self):
        print("Retrieving all symbols")
        symbols = list(Security.objects.values_list('symbol', flat=True))
        print("Retrieved these symbols: ",symbols)
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

            print("information for ", symbol)
            print(info)


            row = {
                'security': symbol,
                'last_price': info.get('currentPrice'),
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

        print(df.head())
        return df

    def create_snapshot_df(self):
        columns = [
            'security', 'last_price', 'bid_price', 'ask_price',
            'bid_size', 'ask_size', 'open_price', 'high_price',
            'low_price', 'volume', 'change_amount', 'change_percent',
            'market_timestamp', 'previous_close'
        ]
        return pd.DataFrame(columns=columns)

    def update_snapshot_data(self):
        if self.market_data.empty:
            print("No market data to update.")
            return

        for _, row in self.market_data.iterrows():
            symbol = row['security']
            print(f"Updating market snapshot for {symbol}")
            print(row)

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
                    'last_price': to_decimal(row['last_price']),
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
                }
            )
        return