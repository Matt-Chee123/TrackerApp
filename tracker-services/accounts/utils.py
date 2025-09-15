from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Portfolio, Holding, Transaction
import pandas as pd
from django.db import connection

def bulk_update_accounts_total_value():
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE portfolio AS acc
            SET net_worth = sub.total + COALESCE(acc.cash_balance, 0), total_market_value = sub.total
            FROM (
                SELECT account_id, SUM(quantity * current_price) AS total
                FROM holding
                GROUP BY account_id
            ) AS sub
            WHERE acc.id = sub.account_id;
        """)






