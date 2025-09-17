from accounts.models import Portfolio, Holding, Transaction, Lot
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
            WITH holdings_sum AS (
                SELECT SUM(average_cost * quantity) AS securities_value
                FROM holdings
                WHERE portfolio_id = %s
            )
            SELECT p.name,
                   p.cash_balance,
                   h.securities_value,
                   (h.securities_value + p.cash_balance) AS net_worth
            FROM portfolio p
            CROSS JOIN holdings_sum h
            WHERE p.id = %s;
            """, [portfolio_id, portfolio_id])
            name, cash_balance, securities_value ,net_worth = cursor.fetchone()
            portfolio_data = {
                'name': name,
                'cash_balance': cash_balance or 0,
                'securities_value': securities_value or 0,
                'net_worth': net_worth or 0
            }
            print("xxxxxxxxxx")
            print(portfolio_data['cash_balance'])
            print("xxxxxxxxxx")
            return portfolio_data

    def get_portfolio_holdings(self, portfolio_id):
        with connection.cursor() as cursor:
            cursor.execute("""
            SELECT name, code_id, state, quantity, current_price, unrealized_gain_loss
             FROM holding
            WHERE account_id = %s;""", [portfolio_id])
            columns = [col[0] for col in cursor.description]
            holdings_data = [
                dict(zip(columns, row)) for row in cursor.fetchall()
            ]
            return holdings_data

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
