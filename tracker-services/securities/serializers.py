from rest_framework import serializers
from .models import Security, PriceHistory

class SecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Security
        fields = [
            'symbol','asset_class','security_type','currency','country','sector','industry','sub_industry','market_cap','last_price','price_updated_at','average_volume'
        ]

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = [
            'security','date','open_price','high_price','low_price','close_price','adjusted_close','volume','dividend_amount','split_ratio'
        ]