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
            for holding in obj.holding_set.all():
                total += (holding.current_price * holding.quantity)
            return total

        def get_total_holdings(self, obj):
            return obj.holding_set.count()

        def get_daily_pnl(self, obj): #TODO Do this one
            return