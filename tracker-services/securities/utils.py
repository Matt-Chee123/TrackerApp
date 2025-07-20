import yfinance as yf
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Security, PriceHistory
import pandas as pd

def get_single_stock(symbol):
    print(f"Retrieving stock data for {symbol}")
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        print(f"Company: {info.get('longName', 'N/A')}")
        print(f"Sector: {info.get('sector', 'N/A')}")
        print(f"Market Cap: ${info.get('marketCap', 'N/A'):,}")

        # Get recent price data
        hist = ticker.history(period="5d")
        if not hist.empty:
            latest_price = hist['Close'].iloc[-1]
            print(f"Latest Price: ${latest_price:.2f}")
            print(f"Data points retrieved: {len(hist)}")
            return True
        else:
            print("No historical data found")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False