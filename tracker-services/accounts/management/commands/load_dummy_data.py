from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Account, Holdings, Transactions
from securities.models import Security, PriceHistory
from decimal import Decimal
import random
from datetime import timedelta, date

User = get_user_model()


class Command(BaseCommand):
    help = 'Load dummy data into the database including securities'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading dummy data...'))

        # Create securities data first
        securities_data = [
            {
                'symbol': 'AAPL',
                'name': 'Apple Inc.',
                'short_name': 'Apple',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': 'INFORMATION_TECHNOLOGY',
                'industry': 'Technology Hardware, Storage & Peripherals',
                'sub_industry': 'Computer Hardware',
                'market_cap': 3500000000000,  # $3.5T
                'shares_outstanding': 15204100000,
                'last_price': Decimal('175.25'),
                'average_volume': 52000000,
            },
            {
                'symbol': 'MSFT',
                'name': 'Microsoft Corporation',
                'short_name': 'Microsoft',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': 'INFORMATION_TECHNOLOGY',
                'industry': 'Software',
                'sub_industry': 'Systems Software',
                'market_cap': 3200000000000,  # $3.2T
                'shares_outstanding': 7433000000,
                'last_price': Decimal('420.50'),
                'average_volume': 24000000,
            },
            {
                'symbol': 'NVDA',
                'name': 'NVIDIA Corporation',
                'short_name': 'NVIDIA',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': 'INFORMATION_TECHNOLOGY',
                'industry': 'Semiconductors & Semiconductor Equipment',
                'sub_industry': 'Semiconductors',
                'market_cap': 2100000000000,  # $2.1T
                'shares_outstanding': 2440000000,
                'last_price': Decimal('875.30'),
                'average_volume': 45000000,
            },
            {
                'symbol': 'META',
                'name': 'Meta Platforms Inc.',
                'short_name': 'Meta',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': 'COMMUNICATION_SERVICES',
                'industry': 'Interactive Media & Services',
                'sub_industry': 'Internet & Direct Marketing Retail',
                'market_cap': 1200000000000,  # $1.2T
                'shares_outstanding': 2550000000,
                'last_price': Decimal('485.75'),
                'average_volume': 15000000,
            },
            {
                'symbol': 'TSLA',
                'name': 'Tesla Inc.',
                'short_name': 'Tesla',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': 'CONSUMER_DISCRETIONARY',
                'industry': 'Automobiles',
                'sub_industry': 'Automobile Manufacturers',
                'market_cap': 800000000000,  # $800B
                'shares_outstanding': 3170000000,
                'last_price': Decimal('248.75'),
                'average_volume': 35000000,
            },
            {
                'symbol': 'AMZN',
                'name': 'Amazon.com Inc.',
                'short_name': 'Amazon',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': 'CONSUMER_DISCRETIONARY',
                'industry': 'Internet & Direct Marketing Retail',
                'sub_industry': 'Internet & Direct Marketing Retail',
                'market_cap': 1600000000000,  # $1.6T
                'shares_outstanding': 10300000000,
                'last_price': Decimal('155.20'),
                'average_volume': 28000000,
            },
            {
                'symbol': 'GOOGL',
                'name': 'Alphabet Inc.',
                'short_name': 'Alphabet',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': 'COMMUNICATION_SERVICES',
                'industry': 'Interactive Media & Services',
                'sub_industry': 'Internet & Direct Marketing Retail',
                'market_cap': 1800000000000,  # $1.8T
                'shares_outstanding': 12800000000,
                'last_price': Decimal('142.65'),
                'average_volume': 22000000,
            },
            {
                'symbol': 'NFLX',
                'name': 'Netflix Inc.',
                'short_name': 'Netflix',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': 'COMMUNICATION_SERVICES',
                'industry': 'Entertainment',
                'sub_industry': 'Movies & Entertainment',
                'market_cap': 180000000000,  # $180B
                'shares_outstanding': 430000000,
                'last_price': Decimal('425.80'),
                'average_volume': 8000000,
            },
            {
                'symbol': 'ADBE',
                'name': 'Adobe Inc.',
                'short_name': 'Adobe',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': 'INFORMATION_TECHNOLOGY',
                'industry': 'Software',
                'sub_industry': 'Application Software',
                'market_cap': 250000000000,  # $250B
                'shares_outstanding': 450000000,
                'last_price': Decimal('565.40'),
                'average_volume': 2500000,
            },
            {
                'symbol': 'CRM',
                'name': 'Salesforce Inc.',
                'short_name': 'Salesforce',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NYSE',
                'country': 'US',
                'sector': 'INFORMATION_TECHNOLOGY',
                'industry': 'Software',
                'sub_industry': 'Application Software',
                'market_cap': 220000000000,  # $220B
                'shares_outstanding': 980000000,
                'last_price': Decimal('275.90'),
                'average_volume': 3500000,
            },
            # Conservative/Value stocks
            {
                'symbol': 'BRK.B',
                'name': 'Berkshire Hathaway Inc.',
                'short_name': 'Berkshire Hathaway',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NYSE',
                'country': 'US',
                'sector': 'FINANCIALS',
                'industry': 'Multi-Sector Holdings',
                'sub_industry': 'Multi-Sector Holdings',
                'market_cap': 900000000000,  # $900B
                'shares_outstanding': 2330000000,
                'last_price': Decimal('385.60'),
                'average_volume': 3200000,
            },
            {
                'symbol': 'JNJ',
                'name': 'Johnson & Johnson',
                'short_name': 'Johnson & Johnson',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NYSE',
                'country': 'US',
                'sector': 'HEALTHCARE',
                'industry': 'Pharmaceuticals',
                'sub_industry': 'Pharmaceuticals',
                'market_cap': 420000000000,  # $420B
                'shares_outstanding': 2400000000,
                'last_price': Decimal('168.45'),
                'average_volume': 6500000,
            },
            {
                'symbol': 'PG',
                'name': 'Procter & Gamble Co.',
                'short_name': 'Procter & Gamble',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NYSE',
                'country': 'US',
                'sector': 'CONSUMER_STAPLES',
                'industry': 'Household Products',
                'sub_industry': 'Household Products',
                'market_cap': 380000000000,  # $380B
                'shares_outstanding': 2350000000,
                'last_price': Decimal('158.75'),
                'average_volume': 5800000,
            },
            {
                'symbol': 'KO',
                'name': 'Coca-Cola Company',
                'short_name': 'Coca-Cola',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NYSE',
                'country': 'US',
                'sector': 'CONSUMER_STAPLES',
                'industry': 'Beverages',
                'sub_industry': 'Soft Drinks',
                'market_cap': 270000000000,  # $270B
                'shares_outstanding': 4310000000,
                'last_price': Decimal('62.30'),
                'average_volume': 12000000,
            },
            {
                'symbol': 'WMT',
                'name': 'Walmart Inc.',
                'short_name': 'Walmart',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NYSE',
                'country': 'US',
                'sector': 'CONSUMER_STAPLES',
                'industry': 'Food & Staples Retailing',
                'sub_industry': 'Hypermarkets & Super Centers',
                'market_cap': 650000000000,  # $650B
                'shares_outstanding': 2700000000,
                'last_price': Decimal('165.85'),
                'average_volume': 8500000,
            },
            # ETFs
            {
                'symbol': 'VOO',
                'name': 'Vanguard S&P 500 ETF',
                'short_name': 'Vanguard S&P 500',
                'asset_class': 'ETF',
                'security_type': 'Exchange Traded Fund',
                'primary_exchange': 'NYSE',
                'country': 'US',
                'sector': None,  # ETFs don't have sectors
                'industry': 'Large Blend',
                'sub_industry': 'Large Blend',
                'market_cap': None,  # ETF market cap is different
                'expense_ratio': Decimal('0.0003'),  # 0.03%
                'fund_family': 'Vanguard',
                'last_price': Decimal('445.20'),
                'average_volume': 4500000,
            },
            {
                'symbol': 'IXUS',
                'name': 'iShares Core MSCI Total International Stock ETF',
                'short_name': 'iShares Total International',
                'asset_class': 'ETF',
                'security_type': 'Exchange Traded Fund',
                'primary_exchange': 'NASDAQ',
                'country': 'US',
                'sector': None,
                'industry': 'Foreign Large Blend',
                'sub_industry': 'Foreign Large Blend',
                'market_cap': None,
                'expense_ratio': Decimal('0.0009'),  # 0.09%
                'fund_family': 'BlackRock',
                'last_price': Decimal('68.45'),
                'average_volume': 350000,
            },
            # Meme stocks (for closed positions)
            {
                'symbol': 'GME',
                'name': 'GameStop Corp.',
                'short_name': 'GameStop',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NYSE',
                'country': 'US',
                'sector': 'CONSUMER_DISCRETIONARY',
                'industry': 'Specialty Retail',
                'sub_industry': 'Computer & Electronics Retail',
                'market_cap': 4500000000,  # $4.5B
                'shares_outstanding': 305000000,
                'last_price': Decimal('15.25'),
                'average_volume': 3200000,
            },
            {
                'symbol': 'AMC',
                'name': 'AMC Entertainment Holdings Inc.',
                'short_name': 'AMC Entertainment',
                'asset_class': 'EQUITY',
                'security_type': 'Common Stock',
                'primary_exchange': 'NYSE',
                'country': 'US',
                'sector': 'COMMUNICATION_SERVICES',
                'industry': 'Entertainment',
                'sub_industry': 'Movies & Entertainment',
                'market_cap': 1600000000,  # $1.6B
                'shares_outstanding': 330000000,
                'last_price': Decimal('4.85'),
                'average_volume': 8500000,
            }
        ]

        # Create securities
        securities = {}
        for security_data in securities_data:
            security, created = Security.objects.get_or_create(
                symbol=security_data['symbol'],
                defaults={
                    **security_data,
                    'price_updated_at': timezone.now()
                }
            )
            if created:
                self.stdout.write(f'Created security: {security.symbol} - {security.name}')

            else:
                self.stdout.write("error")
            securities[security.symbol] = security

        # Generate some sample price history for a few securities
        sample_symbols = ['AAPL', 'MSFT', 'TSLA', 'VOO']

        for symbol in sample_symbols:
            security = securities[symbol]
            current_price = security.last_price

            # Generate 60 days of price history
            for days_ago in range(60, 0, -1):
                price_date = timezone.now().date() - timedelta(days=days_ago)

                # Simple random walk for demo data
                price_change = Decimal(str(random.uniform(-0.05, 0.05)))  # ±5% daily change
                base_price = current_price * (1 + price_change)

                # Generate OHLC data
                open_price = base_price * Decimal(str(random.uniform(0.98, 1.02)))
                high_price = base_price * Decimal(str(random.uniform(1.00, 1.05)))
                low_price = base_price * Decimal(str(random.uniform(0.95, 1.00)))
                close_price = base_price
                volume = random.randint(int(security.average_volume * 0.5), int(security.average_volume * 1.5))

                price_history, created = PriceHistory.objects.get_or_create(
                    security=security,
                    date=price_date,
                    defaults={
                        'open_price': open_price,
                        'high_price': high_price,
                        'low_price': low_price,
                        'close_price': close_price,
                        'adjusted_close': close_price,
                        'volume': volume,
                        'dividend_amount': Decimal('0'),
                        'split_ratio': Decimal('1.0'),
                    }
                )

                if created and days_ago % 10 == 0:  # Print every 10th day
                    self.stdout.write(f'Created price history for {symbol} on {price_date}')

        # Create users (same as before)
        users_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'password': 'testpass123'
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'password': 'testpass123'
            },
            {
                'username': 'bob_wilson',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'password': 'testpass123'
            }
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            users.append(user)

        # Create accounts
        accounts_data = [
            {'account_name': "John's Trading Account", 'user': users[0]},
            {'account_name': "Jane's Investment Portfolio", 'user': users[1]},
            {'account_name': "Bob's Retirement Fund", 'user': users[2]}
        ]

        accounts = []
        for account_data in accounts_data:
            account, created = Account.objects.get_or_create(
                account_name=account_data['account_name'],
                user=account_data['user']
            )
            if created:
                self.stdout.write(f'Created account: {account.account_name}')
            accounts.append(account)

        # Updated holdings data (same structure but references securities)
        holdings_data = [
            # Tech stocks - John's account
            {'code': 'AAPL', 'account': accounts[0], 'quantity': Decimal('50.750000')},
            {'code': 'MSFT', 'account': accounts[0], 'quantity': Decimal('30.000000')},
            {'code': 'NVDA', 'account': accounts[0], 'quantity': Decimal('15.500000')},
            {'code': 'META', 'account': accounts[0], 'quantity': Decimal('25.250000')},

            # Jane's diversified portfolio
            {'code': 'TSLA', 'account': accounts[1], 'quantity': Decimal('20.500000')},
            {'code': 'AMZN', 'account': accounts[1], 'quantity': Decimal('35.000000')},
            {'code': 'GOOGL', 'account': accounts[1], 'quantity': Decimal('40.750000')},
            {'code': 'NFLX', 'account': accounts[1], 'quantity': Decimal('18.000000')},
            {'code': 'ADBE', 'account': accounts[1], 'quantity': Decimal('12.500000')},
            {'code': 'CRM', 'account': accounts[1], 'quantity': Decimal('22.750000')},

            # Bob's conservative retirement portfolio
            {'code': 'BRK.B', 'account': accounts[2], 'quantity': Decimal('45.000000')},
            {'code': 'JNJ', 'account': accounts[2], 'quantity': Decimal('60.250000')},
            {'code': 'PG', 'account': accounts[2], 'quantity': Decimal('35.500000')},
            {'code': 'KO', 'account': accounts[2], 'quantity': Decimal('80.000000')},
            {'code': 'WMT', 'account': accounts[2], 'quantity': Decimal('42.750000')},
            {'code': 'VOO', 'account': accounts[2], 'quantity': Decimal('100.000000')},
            {'code': 'IXUS', 'account': accounts[2], 'quantity': Decimal('75.500000')},

            # Closed positions
            {'code': 'GME', 'account': accounts[0], 'quantity': Decimal('0.000000'), 'state': 'closed'},
            {'code': 'AMC', 'account': accounts[0], 'quantity': Decimal('0.000000'), 'state': 'closed'},
        ]

        # Create holdings with reference to security
        holdings = []
        for holding_data in holdings_data:
            security = securities[holding_data['code']]

            holding, created = Holdings.objects.get_or_create(
                name=security.name,
                code=security,
                account=holding_data['account'],
                defaults={
                    'state': holding_data.get('state', 'active'),
                    'quantity': holding_data['quantity'],
                    'current_price': security.last_price
                }
            )
            if created:
                self.stdout.write(f'Created holding: {holding.name}')
            holdings.append(holding)

        # Rest of transaction creation logic remains the same...
        # [Transaction creation code would go here - same as original]

        self.stdout.write(self.style.SUCCESS('Successfully loaded dummy data with securities!'))

        # Print summary
        self.stdout.write(self.style.SUCCESS('\n--- Summary ---'))
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Accounts: {Account.objects.count()}')
        self.stdout.write(f'Securities: {Security.objects.count()}')
        self.stdout.write(f'Holdings: {Holdings.objects.count()}')
        self.stdout.write(f'Price History Records: {PriceHistory.objects.count()}')

        # Show portfolio breakdown by account
        for account in accounts:
            self.stdout.write(f'\n{account.account_name}:')
            account_holdings = Holdings.objects.filter(account=account, state='active')
            total_value = sum(h.quantity * h.current_price for h in account_holdings)

            for holding in account_holdings:
                security = securities[holding.code.symbol]
                value = holding.quantity * holding.current_price
                weight = (value / total_value * 100) if total_value > 0 else 0
                self.stdout.write(
                    f'  {security.symbol} ({security.sector}): {holding.quantity} shares = ${value:,.2f} ({weight:.1f}%)'
                )