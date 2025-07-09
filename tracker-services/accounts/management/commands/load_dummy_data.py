from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Account, Holdings, Transactions
from decimal import Decimal

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
                user=account_data['user']  # Changed from user_id to user
            )
            if created:
                self.stdout.write(f'Created account: {account.account_name}')
            accounts.append(account)

        # Create holdings
        holdings_data = [
            {
                'name': 'Apple Inc.',
                'code': 'AAPL',
                'account': accounts[0],
                'state': 'active',
                'quantity': Decimal('10.500000'),
                'current_price': Decimal('175.25')
            },
            {
                'name': 'Microsoft Corporation',
                'code': 'MSFT',
                'account': accounts[0],
                'state': 'active',
                'quantity': Decimal('25.000000'),
                'current_price': Decimal('420.50')
            },
            {
                'name': 'Tesla Inc.',
                'code': 'TSLA',
                'account': accounts[1],
                'state': 'active',
                'quantity': Decimal('5.250000'),
                'current_price': Decimal('248.75')
            },
            {
                'name': 'Amazon.com Inc.',
                'code': 'AMZN',
                'account': accounts[1],
                'state': 'active',
                'quantity': Decimal('8.000000'),
                'current_price': Decimal('155.20')
            },
            {
                'name': 'Alphabet Inc.',
                'code': 'GOOGL',
                'account': accounts[2],
                'state': 'active',
                'quantity': Decimal('12.750000'),
                'current_price': Decimal('142.65')
            }
        ]

        holdings = []
        for holding_data in holdings_data:
            holding, created = Holdings.objects.get_or_create(
                name=holding_data['name'],
                code=holding_data['code'],
                account=holding_data['account'],  # Changed from account_id to account
                defaults={
                    'state': holding_data['state'],
                    'quantity': holding_data['quantity'],
                    'current_price': holding_data['current_price']
                }
            )
            if created:
                self.stdout.write(f'Created holding: {holding.name}')
            holdings.append(holding)

        # Create transactions
        transactions_data = [
            {
                'account': accounts[0],  # Changed from portfolio to account
                'holding': holdings[0],
                'transaction_type': 'buy',
                'quantity': Decimal('10.500000'),
                'price': Decimal('175.25'),
                'fees': Decimal('9.99'),
                'transaction_date': timezone.now() - timezone.timedelta(days=30)
            },
            {
                'account': accounts[0],  # Changed from portfolio to account
                'holding': holdings[1],
                'transaction_type': 'buy',
                'quantity': Decimal('25.000000'),
                'price': Decimal('420.50'),
                'fees': Decimal('15.99'),
                'transaction_date': timezone.now() - timezone.timedelta(days=25)
            },
            {
                'account': accounts[1],  # Changed from portfolio to account
                'holding': holdings[2],
                'transaction_type': 'buy',
                'quantity': Decimal('5.250000'),
                'price': Decimal('248.75'),
                'fees': Decimal('12.50'),
                'transaction_date': timezone.now() - timezone.timedelta(days=20)
            },
            {
                'account': accounts[1],  # Changed from portfolio to account
                'holding': holdings[3],
                'transaction_type': 'buy',
                'quantity': Decimal('8.000000'),
                'price': Decimal('155.20'),
                'fees': Decimal('11.25'),
                'transaction_date': timezone.now() - timezone.timedelta(days=15)
            },
            {
                'account': accounts[2],  # Changed from portfolio to account
                'holding': holdings[4],
                'transaction_type': 'buy',
                'quantity': Decimal('12.750000'),
                'price': Decimal('142.65'),
                'fees': Decimal('18.75'),
                'transaction_date': timezone.now() - timezone.timedelta(days=10)
            }
        ]

        for transaction_data in transactions_data:
            transaction, created = Transactions.objects.get_or_create(
                account=transaction_data['account'],  # Changed from portfolio to account
                holding=transaction_data['holding'],
                transaction_type=transaction_data['transaction_type'],
                quantity=transaction_data['quantity'],
                price=transaction_data['price'],
                defaults={
                    'fees': transaction_data['fees'],
                    'transaction_date': transaction_data['transaction_date']
                }
            )
            if created:
                self.stdout.write(
                    f'Created transaction: {transaction.transaction_type} {transaction.quantity} of {transaction.holding.name}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded dummy data!'))