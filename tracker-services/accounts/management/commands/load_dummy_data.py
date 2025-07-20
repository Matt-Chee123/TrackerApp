from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Account, Holdings, Transactions
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Load dummy data into the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading dummy data...'))

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

        # Expanded holdings data with more variety
        holdings_data = [
            # Tech stocks
            {
                'name': 'Apple Inc.',
                'code': 'AAPL',
                'account': accounts[0],
                'state': 'active',
                'quantity': Decimal('50.750000'),
                'current_price': Decimal('175.25')
            },
            {
                'name': 'Microsoft Corporation',
                'code': 'MSFT',
                'account': accounts[0],
                'state': 'active',
                'quantity': Decimal('30.000000'),
                'current_price': Decimal('420.50')
            },
            {
                'name': 'NVIDIA Corporation',
                'code': 'NVDA',
                'account': accounts[0],
                'state': 'active',
                'quantity': Decimal('15.500000'),
                'current_price': Decimal('875.30')
            },
            {
                'name': 'Meta Platforms Inc.',
                'code': 'META',
                'account': accounts[0],
                'state': 'active',
                'quantity': Decimal('25.250000'),
                'current_price': Decimal('485.75')
            },
            # Jane's diversified portfolio
            {
                'name': 'Tesla Inc.',
                'code': 'TSLA',
                'account': accounts[1],
                'state': 'active',
                'quantity': Decimal('20.500000'),
                'current_price': Decimal('248.75')
            },
            {
                'name': 'Amazon.com Inc.',
                'code': 'AMZN',
                'account': accounts[1],
                'state': 'active',
                'quantity': Decimal('35.000000'),
                'current_price': Decimal('155.20')
            },
            {
                'name': 'Alphabet Inc.',
                'code': 'GOOGL',
                'account': accounts[1],
                'state': 'active',
                'quantity': Decimal('40.750000'),
                'current_price': Decimal('142.65')
            },
            {
                'name': 'Netflix Inc.',
                'code': 'NFLX',
                'account': accounts[1],
                'state': 'active',
                'quantity': Decimal('18.000000'),
                'current_price': Decimal('425.80')
            },
            {
                'name': 'Adobe Inc.',
                'code': 'ADBE',
                'account': accounts[1],
                'state': 'active',
                'quantity': Decimal('12.500000'),
                'current_price': Decimal('565.40')
            },
            {
                'name': 'Salesforce Inc.',
                'code': 'CRM',
                'account': accounts[1],
                'state': 'active',
                'quantity': Decimal('22.750000'),
                'current_price': Decimal('275.90')
            },
            # Bob's conservative retirement portfolio
            {
                'name': 'Berkshire Hathaway Inc.',
                'code': 'BRK.B',
                'account': accounts[2],
                'state': 'active',
                'quantity': Decimal('45.000000'),
                'current_price': Decimal('385.60')
            },
            {
                'name': 'Johnson & Johnson',
                'code': 'JNJ',
                'account': accounts[2],
                'state': 'active',
                'quantity': Decimal('60.250000'),
                'current_price': Decimal('168.45')
            },
            {
                'name': 'Procter & Gamble Co.',
                'code': 'PG',
                'account': accounts[2],
                'state': 'active',
                'quantity': Decimal('35.500000'),
                'current_price': Decimal('158.75')
            },
            {
                'name': 'Coca-Cola Company',
                'code': 'KO',
                'account': accounts[2],
                'state': 'active',
                'quantity': Decimal('80.000000'),
                'current_price': Decimal('62.30')
            },
            {
                'name': 'Walmart Inc.',
                'code': 'WMT',
                'account': accounts[2],
                'state': 'active',
                'quantity': Decimal('42.750000'),
                'current_price': Decimal('165.85')
            },
            {
                'name': 'Vanguard S&P 500 ETF',
                'code': 'VOO',
                'account': accounts[2],
                'state': 'active',
                'quantity': Decimal('100.000000'),
                'current_price': Decimal('445.20')
            },
            {
                'name': 'iShares Core MSCI Total International Stock ETF',
                'code': 'IXUS',
                'account': accounts[2],
                'state': 'active',
                'quantity': Decimal('75.500000'),
                'current_price': Decimal('68.45')
            },
            # Some closed positions
            {
                'name': 'GameStop Corp.',
                'code': 'GME',
                'account': accounts[0],
                'state': 'closed',
                'quantity': Decimal('0.000000'),
                'current_price': Decimal('15.25')
            },
            {
                'name': 'AMC Entertainment Holdings Inc.',
                'code': 'AMC',
                'account': accounts[0],
                'state': 'closed',
                'quantity': Decimal('0.000000'),
                'current_price': Decimal('4.85')
            }
        ]

        holdings = []
        for holding_data in holdings_data:
            holding, created = Holdings.objects.get_or_create(
                name=holding_data['name'],
                code=holding_data['code'],
                account=holding_data['account'],
                defaults={
                    'state': holding_data['state'],
                    'quantity': holding_data['quantity'],
                    'current_price': holding_data['current_price']
                }
            )
            if created:
                self.stdout.write(f'Created holding: {holding.name}')
            holdings.append(holding)

        # Generate more realistic transactions with multiple buys/sells
        transactions_data = []

        # John's trading activity (more frequent trading)
        john_holdings = [h for h in holdings if h.account == accounts[0]]
        for holding in john_holdings:
            if holding.state == 'active':
                # Initial buy
                transactions_data.append({
                    'account': accounts[0],
                    'holding': holding,
                    'transaction_type': 'buy',
                    'quantity': Decimal(str(round(float(holding.quantity) * 0.6, 6))),
                    'price': holding.current_price - Decimal(str(random.uniform(5, 20))),
                    'fees': Decimal(str(round(random.uniform(9.99, 19.99), 2))),
                    'transaction_date': timezone.now() - timezone.timedelta(days=random.randint(60, 120))
                })

                # Additional buy
                transactions_data.append({
                    'account': accounts[0],
                    'holding': holding,
                    'transaction_type': 'buy',
                    'quantity': Decimal(str(round(float(holding.quantity) * 0.4, 6))),
                    'price': holding.current_price - Decimal(str(random.uniform(1, 10))),
                    'fees': Decimal(str(round(random.uniform(9.99, 15.99), 2))),
                    'transaction_date': timezone.now() - timezone.timedelta(days=random.randint(20, 40))
                })

                # Sometimes a partial sell
                if random.choice([True, False]):
                    transactions_data.append({
                        'account': accounts[0],
                        'holding': holding,
                        'transaction_type': 'sell',
                        'quantity': Decimal(str(round(float(holding.quantity) * 0.2, 6))),
                        'price': holding.current_price + Decimal(str(random.uniform(1, 5))),
                        'fees': Decimal(str(round(random.uniform(9.99, 15.99), 2))),
                        'transaction_date': timezone.now() - timezone.timedelta(days=random.randint(5, 15))
                    })
            else:  # Closed positions
                # Buy and then sell all
                buy_quantity = Decimal(str(round(random.uniform(10, 50), 6)))
                buy_price = holding.current_price + Decimal(str(random.uniform(10, 50)))

                transactions_data.append({
                    'account': accounts[0],
                    'holding': holding,
                    'transaction_type': 'buy',
                    'quantity': buy_quantity,
                    'price': buy_price,
                    'fees': Decimal(str(round(random.uniform(9.99, 19.99), 2))),
                    'transaction_date': timezone.now() - timezone.timedelta(days=random.randint(90, 180))
                })

                transactions_data.append({
                    'account': accounts[0],
                    'holding': holding,
                    'transaction_type': 'sell',
                    'quantity': buy_quantity,
                    'price': holding.current_price,
                    'fees': Decimal(str(round(random.uniform(9.99, 19.99), 2))),
                    'transaction_date': timezone.now() - timezone.timedelta(days=random.randint(30, 60))
                })

        # Jane's investment activity (less frequent, larger positions)
        jane_holdings = [h for h in holdings if h.account == accounts[1]]
        for holding in jane_holdings:
            # Dollar cost averaging - multiple smaller buys
            for i in range(random.randint(2, 4)):
                transactions_data.append({
                    'account': accounts[1],
                    'holding': holding,
                    'transaction_type': 'buy',
                    'quantity': Decimal(str(round(float(holding.quantity) / 3, 6))),
                    'price': holding.current_price - Decimal(str(random.uniform(0, 15))),
                    'fees': Decimal(str(round(random.uniform(9.99, 15.99), 2))),
                    'transaction_date': timezone.now() - timezone.timedelta(days=random.randint(30 * i, 30 * (i + 1)))
                })

        # Bob's retirement fund (buy and hold strategy)
        bob_holdings = [h for h in holdings if h.account == accounts[2]]
        for holding in bob_holdings:
            # Single large purchase or few purchases
            for i in range(random.randint(1, 2)):
                transactions_data.append({
                    'account': accounts[2],
                    'holding': holding,
                    'transaction_type': 'buy',
                    'quantity': Decimal(str(round(float(holding.quantity) / (i + 1), 6))),
                    'price': holding.current_price - Decimal(str(random.uniform(5, 25))),
                    'fees': Decimal(str(round(random.uniform(9.99, 25.99), 2))),
                    'transaction_date': timezone.now() - timezone.timedelta(
                        days=random.randint(180 + (i * 30), 360 + (i * 30)))
                })

        # Create transactions
        for transaction_data in transactions_data:
            transaction, created = Transactions.objects.get_or_create(
                account=transaction_data['account'],
                holding=transaction_data['holding'],
                transaction_type=transaction_data['transaction_type'],
                quantity=transaction_data['quantity'],
                price=transaction_data['price'],
                transaction_date=transaction_data['transaction_date'],
                defaults={
                    'fees': transaction_data['fees']
                }
            )
            if created:
                self.stdout.write(
                    f'Created transaction: {transaction.transaction_type} {transaction.quantity} of {transaction.holding.name} on {transaction.transaction_date.date()}'
                )

        self.stdout.write(self.style.SUCCESS('Successfully loaded dummy data!'))

        # Print summary
        self.stdout.write(self.style.SUCCESS('\n--- Summary ---'))
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Accounts: {Account.objects.count()}')
        self.stdout.write(f'Holdings: {Holdings.objects.count()}')
        self.stdout.write(f'Transactions: {Transactions.objects.count()}')

        for account in accounts:
            active_holdings = Holdings.objects.filter(account=account, state='active').count()
            total_transactions = Transactions.objects.filter(account=account).count()
            self.stdout.write(
                f'{account.account_name}: {active_holdings} active holdings, {total_transactions} transactions')