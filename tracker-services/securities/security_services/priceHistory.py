import yfinance as yf
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from ..models import Security, PriceHistory
import pandas as pd


class PriceHistoryService:

    @staticmethod
    def update_price_history():
        print("here")
        pass

    @staticmethod
    def map_sector(sector):
        sector_mapping = {
            'Energy': 'ENERGY',
            'Basic Materials': 'MATERIALS',
            'Industrials': 'INDUSTRIALS',
            'Consumer Cyclical': 'CONSUMER_DISCRETIONARY',
            'Consumer Defensive': 'CONSUMER_STAPLES',
            'Healthcare': 'HEALTHCARE',
            'Financial Services': 'FINANCIALS',
            'Financial': 'FINANCIALS',
            'Technology': 'INFORMATION_TECHNOLOGY',
            'Communication Services': 'COMMUNICATION_SERVICES',
            'Utilities': 'UTILITIES',
            'Real Estate': 'REAL_ESTATE',
        }
        return sector_mapping.get(sector, None)

    @staticmethod
    def get_asset_class(type):
        quote_type = type.upper()

        if quote_type == 'EQUITY':
            return 'EQUITY'
        elif quote_type == 'ETF':
            return 'ETF'
        elif quote_type == 'MUTUALFUND':
            return 'MUTUAL_FUND'
        elif quote_type == 'INDEX':
            return 'INDEX'
        else:
            return 'EQUITY'

    @staticmethod
    def update_stock_price(symbol):
        print(f"Updating stock data for {symbol}")
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info

            sector = SecurityService.map_sector(info.get('sector'))
            asset_class = SecurityService.get_asset_class(info.get('quoteType', ''))

            security, created = Security.objects.get_or_create(
                symbol=symbol,
                defaults={
                    'name': info.get('longName', info.get('shortName', symbol)),
                    'short_name': info.get('shortName', ''),
                    'asset_class': asset_class,
                    'security_type': info.get('quoteType', ''),
                    'primary_exchange': info.get('exchange', ''),
                    'currency': info.get('currency', 'USD'),
                    'country': info.get('country', 'US'),
                    'sector': sector,
                    'industry': info.get('industry', ''),
                    'market_cap': info.get('marketCap'),
                    'shares_outstanding': info.get('sharesOutstanding'),
                    'expense_ratio': Decimal(str(info.get('expenseRatio', 0))) if info.get('expenseRatio') else None,
                    'fund_family': info.get('fundFamily', ''),
                    'average_volume': info.get('averageVolume'),
                    'is_actively_traded': True,
                    'data_source': 'yfinance',
                }
            )

            if not created:
                security.name = info.get('longName', info.get('shortName', security.name))
                security.short_name = info.get('shortName', security.short_name)
                security.sector = sector or security.sector
                security.industry = info.get('industry', security.industry)
                security.market_cap = info.get('marketCap') or security.market_cap
                security.shares_outstanding = info.get('sharesOutstanding') or security.shares_outstanding
                security.average_volume = info.get('averageVolume') or security.average_volume

                if info.get('expenseRatio'):
                    security.expense_ratio = Decimal(str(info.get('expenseRatio')))

                security.fund_family = info.get('fundFamily', security.fund_family)
                security.updated_at = timezone.now()

            hist = ticker.history(period="30d", auto_adjust=False)

            if not hist.empty:
                latest_close = hist['Close'].iloc[-1]
                security.last_price = Decimal(str(latest_close))
                security.price_updated_at = timezone.now()
                security.save()

                updated_count = 0
                for date, row in hist.iterrows():
                    price_date = date.date()

                    price_history, created = PriceHistory.objects.update_or_create(
                        security=security,
                        date=price_date,
                        defaults={
                            'open_price': Decimal(str(row['Open'])),
                            'high_price': Decimal(str(row['High'])),
                            'low_price': Decimal(str(row['Low'])),
                            'close_price': Decimal(str(row['Close'])),
                            'adjusted_close': Decimal(str(row['Adj Close'])),
                            'volume': int(row['Volume']) if pd.notna(row['Volume']) else 0,
                            'dividend_amount': Decimal('0'),
                            'split_ratio': Decimal('1.0'),
                        }
                    )
                    if created:
                        updated_count += 1

                print(f"Successfully updated {symbol}: {updated_count} new price records, {len(hist)} total")
                return True
            else:
                security.save()
                print(f"Updated {symbol} info but no historical data found")
                return True

        except Exception as e:
            print(f"Error: {e}")
            return False

    @staticmethod
    def get_dividend_and_split_data(symbol, start_date=None):
        if start_date is None:
            start_date = datetime.now() - timedelta(days=365)

        try:
            ticker = yf.Ticker(symbol)
            security = Security.objects.get(symbol=symbol)

            dividends = ticker.dividends
            if not dividends.empty:
                dividends_since_start = dividends[dividends.index >= start_date]

                for date, dividend_amount in dividends_since_start.items():
                    try:
                        price_record = PriceHistory.objects.get(
                            security=security,
                            date=date.date()
                        )
                        price_record.dividend_amount = Decimal(str(dividend_amount))
                        price_record.save()
                    except PriceHistory.DoesNotExist:
                        pass

            splits = ticker.splits
            if not splits.empty:
                splits_since_start = splits[splits.index >= start_date]

                for date, split_ratio in splits_since_start.items():
                    try:
                        price_record = PriceHistory.objects.get(
                            security=security,
                            date=date.date()
                        )
                        price_record.split_ratio = Decimal(str(split_ratio))
                        price_record.save()
                    except PriceHistory.DoesNotExist:
                        pass

            return True

        except Exception as e:
            print(f"Error getting dividend/split data for {symbol}: {e}")
            return False

    @staticmethod
    def bulk_update_securities():
        results = {}
        symbols = SecurityService.get_all_symbols()
        for symbol in symbols:
            results[symbol] = SecurityService.update_stock_price(symbol)
        return results

    @staticmethod
    def bulk_update_dividends_and_splits(symbols):
        results = {}
        for symbol in symbols:
            results[symbol] = SecurityService.get_dividend_and_split_data(symbol)
        return results


    @staticmethod
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

    @staticmethod
    def get_all_symbols():
        print("Retrieving all symbols")
        symbols = list(Security.objects.values_list('symbol', flat=True))
        print("Retrieved these symbols: ",symbols)
        return symbols