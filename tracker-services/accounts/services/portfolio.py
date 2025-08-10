from decimal import Decimal
from django.utils import timezone
from accounts.models import Account, Holdings, Lots, Security, Transactions
from securities.models import Security
from django.db import connection


class PortfolioService:


    @staticmethod
    def calculate_holding_pnl():

        holdings = PortfolioService.get_all_holdings()
        for holding in holdings:
            lots = PortfolioService.get_all_lots_for_holding(holding['id'])
            unrealised_pnl = PortfolioService.calculate_unrealised_pnl(holding,lots)
            print(unrealised_pnl)
            PortfolioService.update_holding_pnl(holding['id'], unrealised_pnl)

    @staticmethod
    def get_current_market_price():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM security
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_all_holdings():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM holdings
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def get_all_lots_for_holding(holding):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM lots WHERE holding_id = %s AND is_closed = false
            """, [holding])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    @staticmethod
    def update_holding_pnl(holding, value):
        with connection.cursor() as cursor:
            cursor.execute("""
            UPDATE holdings
            SET unrealized_gain_loss = %s, last_updated = NOW()
            WHERE holdings.id = %s;
                        """, [value, holding])

    @staticmethod
    def calculate_unrealised_pnl(holding,lots):
        total_cost = 0
        for lot in lots:
            total_cost += lot['total_cost']
        return (holding['current_price'] * holding['quantity']) - total_cost