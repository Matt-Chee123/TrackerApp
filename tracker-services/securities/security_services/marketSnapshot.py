import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, PriceHistory
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

            hist = ticker.history(period="1d", interval="1m")
            print("information for ", symbol)
            print(info)
            print("history for ", symbol)
            print(hist)
            latest_data = hist.iloc[-1]

            row = {
                'security': symbol,
                'last_price': info.get('currentPrice') or latest_data['Close'],
                'bid_price': info.get('bid'),
                'ask_price': info.get('ask'),
                'bid_size': info.get('bidSize'),
                'ask_size': info.get('askSize'),
                'open_price': info.get('open') or latest_data['Open'],
                'high_price': info.get('dayHigh') or latest_data['High'],
                'low_price': info.get('dayLow') or latest_data['Low'],
                'volume': info.get('volume') or int(latest_data['Volume']),
                'change_amount': 0, #TODO
                'change_percent': 0, #TODO
                'market_timestamp': timezone.now(),
                'previous_close': info.get('previousClose'),
            }

            df.loc[len(df)] = row

        print(df.head())
        return tickers

    def create_snapshot_df(self):
        columns = [
            'security', 'last_price', 'bid_price', 'ask_price',
            'bid_size', 'ask_size', 'open_price', 'high_price',
            'low_price', 'volume', 'change_amount', 'change_percent',
            'market_timestamp', 'previous_close'
        ]
        return pd.DataFrame(columns=columns)
