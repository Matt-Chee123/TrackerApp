import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, MarketSnapshot, RiskMetrics
import pandas as pd
import math


class RiskMetricsService:

    def __init__(self):
        self.symbols = self.get_all_symbols()

    def get_all_symbols(self):
        symbols = list(Security.objects.values_list('symbol', flat=True))
        return symbols
