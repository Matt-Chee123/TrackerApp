from decimal import Decimal
from django.utils import timezone
from accounts.models import Account, Holdings, Lots, Security, Transactions
from securities.models import Security
from django.db import connection


class PortfolioService:

    def __init__(self):
        self.user_data = self.get_all_user_data()
        return

    def get_all_user_data(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT user_id, id FROM portfolio;
             """)

            rows = cursor.fetchall()
            print(rows)
        return rows

    def update_portfolio_stats(self):
        self.update_holdings_stats()
        self.update_account_stats()
        return

    def update_account_stats(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH holdings_stats AS (
                  SELECT
                    h.account_id AS account,
					SUM(h.current_price * h.quantity) AS total_value,
					SUM(h.unrealized_gain_loss) AS gain,
					SUM(h.total_cost_basis) AS total_cost
                  FROM holdings h
				  GROUP BY h.account_id
                                )
                UPDATE portfolio
                SET
                  total_market_value = hs.total_value,
				  unrealized_gain_loss = hs.gain,
				  net_worth = hs.total_value + cash_balance,
				  unrealized_gain_loss_pct = CASE
				    WHEN hs.total_cost > 0 THEN hs.gain / hs.total_cost * 100
                    ELSE 0
				END
                FROM holdings_stats hs
                WHERE portfolio.id = hs.account
                ;
            """)

    def update_holdings_stats(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                WITH lot_unrealised AS (
                  SELECT
                    l.holding_id AS holding,
                    SUM((s.last_price - l.purchase_price) * l.remaining_quantity) AS unrealised_pnl,
                    SUM(l.remaining_quantity * l.purchase_price + l.fees) AS total_cost,
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
                  last_updated = NOW(),
				  total_cost_basis = lu.total_cost,
                  unrealized_gain_loss = lu.unrealised_pnl,
                  unrealized_gain_loss_pct = CASE
                    WHEN lu.total_cost > 0 THEN lu.unrealised_pnl / lu.total_cost * 100
                    ELSE 0
                  END
                FROM lot_unrealised lu,
                     security s
                WHERE holdings.id = lu.holding
                AND holdings.code_id = s.symbol;
            """)

    def update_holdings_from_prices(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM holdings
            """)

    def calculate_holding_pnl(self):

        holdings = self.get_all_holdings()
        for holding in holdings:
            lots = self.get_all_lots_for_holding(holding['id'])
            unrealised_pnl = self.calculate_unrealised_pnl(holding,lots)
            self.update_holding_pnl(holding['id'], unrealised_pnl)

    def get_current_market_price(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM security
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    def get_all_holdings(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM holdings
            """)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    def get_all_lots_for_holding(self, holding):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM lots WHERE holding_id = %s AND is_closed = false
            """, [holding])
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]

    def update_holding_pnl(self,holding, value):
        with connection.cursor() as cursor:
            cursor.execute("""
            UPDATE holdings
            SET unrealized_gain_loss = %s, last_updated = NOW()
            WHERE holdings.id = %s;
                        """, [value, holding])

    def calculate_unrealised_pnl(self, holding,lots):
        total_cost = 0
        for lot in lots:
            total_cost += lot['total_cost']
        return (holding['current_price'] * holding['quantity']) - total_cost