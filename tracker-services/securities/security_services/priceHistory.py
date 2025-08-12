import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, PriceHistory
import pandas as pd


class PriceHistoryService:

    def __init__(self):
        self.symbols = self.get_all_symbols()

    def update_price_history(self):
        print("here")
        print(self.symbols)
        pass


    def get_all_symbols(self):
        print("Retrieving all symbols")
        symbols = list(Security.objects.values_list('symbol', flat=True))
        print("Retrieved these symbols: ",symbols)
        return symbols