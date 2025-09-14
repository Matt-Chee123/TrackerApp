from accounts.models import Account, Holdings, Transactions, Lots
from securities.models import Security
from django.db import connection, transaction
from django.utils import timezone


class PortfolioService:
    def __init(self):
        return

    def create_portfolio(self, name, user, initial_cash):
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO portfolio (account_name, user_id, cash_balance) 
                VALUES (%s,%s,%s) 
                RETURNING id;
            """, [name, user, initial_cash])
            portfolio_id = cursor.fetchone()[0]
            return portfolio_id

    def get_portfolio_value(self, portfolio_id):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT account_name, cash_balance, total_market_value, net_worth 
                FROM portfolio WHERE id = %s;
            """, [portfolio_id])
            portfolio_data = cursor.fetchone()
            return portfolio_data

    @transaction.atomic
    def add_holding(self, account_id, symbol, quantity, price, fees=0, transaction_date=None):
        transaction_date = transaction_date or timezone.now()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT name FROM security WHERE symbol = %s;
            """, [symbol])
            security_name = cursor.fetchone[0]
            #TODO: check if holding already exists, if so add to that, if not create a new one
            # then create lot and transaction for this

    def add_transaction(self):
        return

    def add_lot(self):
        return

    def remove_holding(self):
        return

    def remove_lot(self):
        return
