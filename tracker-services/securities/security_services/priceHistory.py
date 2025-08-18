import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, PriceHistory
import pandas as pd
from datetime import date, timedelta

class PriceHistoryService:
 #TODO: check this is working as only 4 symbols being updates
    def __init__(self):
        self.symbols = self.get_all_symbols()
        self.current_date = date.today()
        self.data = self.get_security_data()

    def update_price_history(self):

        for symbol in self.symbols:
            print(symbol)
            info = self.data[symbol]
            print(info)
            day_return = self.get_1d_return(info)
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
                }
            )
        pass

    def get_1d_return(self, data):
        pass

    def get_security_data(self):
        if not self.symbols:
            print("No symbols found.")
            return

        tomorrow = self.current_date + timedelta(days=1)  # end date is exclusive in yfinance

        print(f"Downloading price history for {self.current_date} for: {self.symbols}")

        df = yf.download(
            tickers=" ".join(self.symbols),
            start=self.current_date,
            end=tomorrow,
            interval="1d",
            group_by="ticker",
            auto_adjust=False,
            threads=True
        )

        print("\n=== DataFrame head ===")
        print(df.head())

        # Show structure of columns and data types
        print("\n=== DataFrame info ===")
        print(df.info())

        # Show just the column names
        print("\n=== Columns ===")
        print(df.columns)
        return df

    def get_all_symbols(self):
        print("Retrieving all symbols")
        symbols = list(Security.objects.values_list('symbol', flat=True))
        print("Retrieved these symbols: ",symbols)
        return symbols