# management/commands/load_dummy_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Portfolio, Holding, Transaction, Lot, PortfolioSnapshot
from securities.models import Security, PriceHistory
from core.services.portfolio_service import PortfolioService
from decimal import Decimal
import random
from datetime import timedelta, date
import yfinance as yf

User = get_user_model()


class Command(BaseCommand):
    help = 'Load dummy data into the database including securities and clean portfolio data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading dummy data with clean models...'))

        # Create securities data (same as before)
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
                'market_cap': 3500000000000,
                'shares_outstanding': 15204100000,
                'current_price': Decimal('175.25'),  # Renamed from current_price
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
                'market_cap': 3200000000000,
                'shares_outstanding': 7433000000,
                'current_price': Decimal('420.50'),
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
                'market_cap': 2100000000000,
                'shares_outstanding': 2440000000,
                'current_price': Decimal('875.30'),
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
                'market_cap': 1200000000000,
                'shares_outstanding': 2550000000,
                'current_price': Decimal('485.75'),
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
                'market_cap': 800000000000,
                'shares_outstanding': 3170000000,
                'current_price': Decimal('248.75'),
                'average_volume': 35000000,
            },
            # Add more securities as needed...
        ]

        # Create securities
        securities = {}
        for security_data in securities_data:
            security, created = Security.objects.get_or_create(
                symbol=security_data['symbol'],
                defaults={
                    **security_data,
                    'updated_at': timezone.now()  # Updated field name
                }
            )
            if created:
                self.stdout.write(f'Created security: {security.symbol} - {security.name}')
            securities[security.symbol] = security

        # Create price history (simplified version)
        self._create_price_history(securities)

        # Create users
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

        # Create portfolios (renamed from accounts)
        portfolio_data = [
            {
                'name': "John's Trading Account",
                'user': users[0],
                'cash_balance': Decimal('10000.00'),
                'drift_threshold': Decimal('0.05')
            },
            {
                'name': "Jane's Investment Portfolio",
                'user': users[1],
                'cash_balance': Decimal('25000.00'),
                'drift_threshold': Decimal('0.03')
            },
            {
                'name': "Bob's Retirement Fund",
                'user': users[2],
                'cash_balance': Decimal('50000.00'),
                'drift_threshold': Decimal('0.02')
            }
        ]

        portfolios = []
        for data in portfolio_data:
            portfolio, created = Portfolio.objects.get_or_create(
                name=data['name'],
                user=data['user'],
                defaults={
                    'cash_balance': data['cash_balance'],
                    'drift_threshold': data['drift_threshold']
                }
            )
            if created:
                self.stdout.write(f'Created portfolio: {portfolio.name}')
            portfolios.append(portfolio)

        # Create holdings with proper cost basis
        holdings_data = [
            # John's tech-heavy portfolio
            {
                'security': 'AAPL',
                'portfolio': portfolios[0],
                'quantity': Decimal('50.750000'),
                'average_cost': Decimal('165.30'),  # Bought at lower price
                'target_weight': Decimal('0.25'),  # 25% target
            },
            {
                'security': 'MSFT',
                'portfolio': portfolios[0],
                'quantity': Decimal('30.000000'),
                'average_cost': Decimal('380.50'),
                'target_weight': Decimal('0.30'),
            },
            {
                'security': 'NVDA',
                'portfolio': portfolios[0],
                'quantity': Decimal('15.500000'),
                'average_cost': Decimal('820.75'),
                'target_weight': Decimal('0.20'),
            },
            {
                'security': 'META',
                'portfolio': portfolios[0],
                'quantity': Decimal('25.250000'),
                'average_cost': Decimal('450.20'),
                'target_weight': Decimal('0.25'),
            },

            # Jane's diversified portfolio  
            {
                'security': 'TSLA',
                'portfolio': portfolios[1],
                'quantity': Decimal('20.500000'),
                'average_cost': Decimal('220.40'),
                'target_weight': Decimal('0.15'),
            },
            {
                'security': 'AAPL',
                'portfolio': portfolios[1],
                'quantity': Decimal('35.000000'),
                'average_cost': Decimal('155.80'),
                'target_weight': Decimal('0.20'),
            },
            {
                'security': 'MSFT',
                'portfolio': portfolios[1],
                'quantity': Decimal('25.750000'),
                'average_cost': Decimal('395.60'),
                'target_weight': Decimal('0.25'),
            },
        ]

        # Create holdings
        holdings = []
        for holding_data in holdings_data:
            security = securities[holding_data['security']]

            holding, created = Holding.objects.get_or_create(
                portfolio=holding_data['portfolio'],
                security=security,
                defaults={
                    'quantity': holding_data['quantity'],
                    'average_cost': holding_data['average_cost'],
                    'target_weight': holding_data.get('target_weight'),
                    'state': 'active'
                }
            )
            if created:
                self.stdout.write(f'Created holding: {security.symbol} in {holding.portfolio.name}')
            holdings.append(holding)

        # Create transactions for each holding
        for holding in holdings:
            # Create initial buy transaction
            buy_transaction = Transaction.objects.create(
                portfolio=holding.portfolio,
                holding=holding,
                transaction_type='buy',
                quantity=holding.quantity,
                price=holding.average_cost,
                amount=holding.quantity * holding.average_cost,
                fees=Decimal('9.99'),
                transaction_date=timezone.now() - timedelta(days=random.randint(30, 180)),
                description=f'Initial purchase of {holding.security.symbol}'
            )
            self.stdout.write(f'Created buy transaction for {holding.security.symbol}')

            # Create tax lots for each holding
            self._create_tax_lots(holding)

        # Create some cash transactions
        for portfolio in portfolios:
            # Initial deposit
            Transaction.objects.create(
                portfolio=portfolio,
                transaction_type='deposit',
                amount=portfolio.cash_balance,
                transaction_date=timezone.now() - timedelta(days=200),
                description='Initial cash deposit'
            )

        # Create historical snapshots
        self._create_portfolio_snapshots(portfolios, securities)

        self.stdout.write(self.style.SUCCESS('Successfully loaded clean dummy data!'))

    def _create_price_history(self, securities):
        """Create simplified price history"""
        end_date = timezone.now().date()

        for symbol, security in securities.items():
            # Create 30 days of price history
            for i in range(30):
                price_date = end_date - timedelta(days=i)

                # Simple price variation
                base_price = float(security.current_price)
                daily_change = random.uniform(-0.05, 0.05)  # ±5% daily change
                close_price = base_price * (1 + daily_change)

                PriceHistory.objects.get_or_create(
                    security=security,
                    date=price_date,
                    defaults={
                        'close_price': Decimal(str(close_price)),
                        'open_price': Decimal(str(close_price * 0.995)),
                        'high_price': Decimal(str(close_price * 1.02)),
                        'low_price': Decimal(str(close_price * 0.98)),
                        'volume': random.randint(1000000, 50000000)
                    }
                )

    def _create_tax_lots(self, holding):
        """Create 1-2 tax lots per holding"""
        total_quantity = holding.quantity

        if total_quantity > Decimal('20'):
            # Split into 2 lots
            lot1_qty = total_quantity * Decimal('0.6')
            lot2_qty = total_quantity - lot1_qty

            lots_data = [
                {
                    'quantity': lot1_qty,
                    'price': holding.average_cost * Decimal('0.95'),  # Bought earlier, cheaper
                    'date_offset': 120
                },
                {
                    'quantity': lot2_qty,
                    'price': holding.average_cost * Decimal('1.05'),  # Bought later, more expensive
                    'date_offset': 60
                }
            ]
        else:
            # Single lot
            lots_data = [
                {
                    'quantity': total_quantity,
                    'price': holding.average_cost,
                    'date_offset': 90
                }
            ]

        for lot_data in lots_data:
            fees = Decimal('4.99')  # Split fees across lots
            total_cost = (lot_data['quantity'] * lot_data['price']) + fees

            Lot.objects.create(
                holding=holding,
                quantity=lot_data['quantity'],
                remaining_quantity=lot_data['quantity'],
                purchase_price=lot_data['price'],
                purchase_date=timezone.now() - timedelta(days=lot_data['date_offset']),
                total_cost=total_cost,
                fees=fees
            )

    def _create_portfolio_snapshots(self, portfolios, securities):
        """Create 30 days of portfolio snapshots"""
        portfolio_service = PortfolioService()

        # Create snapshots for last 30 days
        for i in range(30):
            snapshot_date = timezone.now().date() - timedelta(days=i)

            for portfolio in portfolios:
                # Calculate portfolio value for this date
                # (In real implementation, would use historical prices)
                portfolio_value = portfolio_service.get_portfolio_value(portfolio.id)
                print(portfolio_value)

                PortfolioSnapshot.objects.get_or_create(
                    portfolio=portfolio,
                    date=snapshot_date,
                    defaults={
                        'total_value': int(portfolio_value['net_worth']),
                        'cash_balance': int(portfolio_value['cash_balance']),
                        'securities_value': int(portfolio_value['securities_value'])
                    }
                )

