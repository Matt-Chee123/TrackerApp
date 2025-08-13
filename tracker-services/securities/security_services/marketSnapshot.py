import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, PriceHistory
import pandas as pd
from datetime import date, timedelta

class MarketSnapshotService:

    def __init__(self):
        pass