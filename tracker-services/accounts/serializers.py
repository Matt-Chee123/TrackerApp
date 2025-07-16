from rest_framework import serializers
from .models import Account, Holdings, Transactions

class AccountSerializer(serializers.ModelSerializer):
    total_value = serializers.SerializerMethodField()
    total_holdings = serializers.SerializerMethodField()
    daily_pnl = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = [
            'id','account_name','user','total_value','total_holdings','daily_pnl'
        ]

    def get_total_value(self, obj):
        total = 0
        for holding in obj.holdings_set.all():
            total += (holding.current_price * holding.quantity)
        return total

    def get_total_holdings(self, obj):
        return obj.holdings_set.count()

    def get_daily_pnl(self, obj): #TODO Do this one
        return

class TransactionsSerializer(serializers.ModelSerializer):
    total_value = serializers.SerializerMethodField()
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)

    class Meta:
        model = Transactions
        fields = [
            'id', 'transaction_type', 'transaction_type_display', 'quantity',
            'price', 'fees', 'transaction_date', 'created_date',
            'total_value'
        ]

    def get_total_value(self, obj):
        return (obj.quantity * obj.price) + obj.fees


class HoldingsSerializer(serializers.ModelSerializer):
    current_value = serializers.SerializerMethodField()
    total_cost = serializers.SerializerMethodField()
    unrealized_pnl = serializers.SerializerMethodField()

    class Meta:
        model = Holdings
        fields = [
            'id', 'name', 'code', 'state', 'quantity', 'current_price',
            'created_date', 'last_updated',
            'current_value', 'total_cost', 'unrealized_pnl'
        ]
        read_only_fields = ['created_date', 'last_updated']

    def get_current_value(self, obj):
        return (obj.current_price * obj.quantity)

    def get_total_cost(self, obj):
        buy_transactions = obj.transactions_set.filter(transaction_type='buy')
        cost = 0
        for tx in buy_transactions:
            cost += (tx.quantity * tx.price) + tx.fees
        return cost

    def get_unrealized_pnl(self, obj):
        current_value = self.get_current_value(obj)
        total_cost = self.get_total_cost(obj)
        return current_value - total_cost

