from decimal import Decimal
from django.utils import timezone
from accounts.models import Account, Holdings, Lots, Security, Transactions
from securities.models import Security
from django.db import connection


class PortfolioService:


    @staticmethod
    def update_portfolio_stats():
        pass

    @staticmethod
    def update_holdings_stats():
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH lot_unrealised AS (
                  SELECT
                    l.holding_id AS holding,
                    SUM((s.last_price - l.purchase_price) * l.remaining_quantity) AS unrealised_pnl,
                    SUM(l.remaining_quantity * l.purchase_price) AS total_cost,
                    SUM(l.remaining_quantity) AS quantity
                  FROM lots l
                  JOIN holdings h ON h.id = l.holding_id
                  JOIN security s ON h.code_id = s.symbol
                  WHERE l.is_closed = false
                  GROUP BY l.holding_id
                )
                UPDATE holdings
                SET
                  current_price = s.last_price,
                  quantity = lu.quantity,
                  unrealized_gain_loss = lu.unrealised_pnl,
                  unrealized_gain_loss_pct = CASE
                    WHEN lu.total_cost > 0 THEN lu.unrealised_pnl / lu.total_cost * 100
                    ELSE 0
                  END
                FROM lot_unrealised lu,
                     security s
                WHERE holdings.id = lu.holding
                AND holdings.code_id = s.symbol
            """)

    @staticmethod
    def update_holdings_from_prices():
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM holdings
            """)

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