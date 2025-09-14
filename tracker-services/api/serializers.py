from rest_framework import serializers
from portfolio.models import Account, Holding
from securities.models import Security

class SecuritySerializer:
    class Meta:
        model = Security
        fields = ["symbol","isin","cusip","cusip","short_name"
            ,"asset_class","security_type","primary_exchange","currency","country"
            ,"sector","industry","sub_industry","market_cap","shares_outstanding"
            ,"maturity_date","coupon_rate","credit_rating","expense_ratio"
            ,"fund_family","is_actively_traded","average_volume","average_volume"
            ,"data_source","created_at","updated_at",]

class PortfolioSerializer:
    class Meta:
        model = Account
        fields = ["id","account_name","user","total_market_value"
            ,"cash_balance","net_worth","unrealized_gain_loss"
            ,"unrealized_gain_loss_pct","last_rebalance_date"
            ,"drift_threshold"]

class HoldingSerializer:
    class Meta:
        model = Holding
        fields = ["name","code","account","state","quantity"
            ,"current_price","created_at","created_date","last_updated"
            ,"target_weight","actual_weight","last_rebalance_date"
            ,"average_cost","total_cost_basis","unrealized_gain_loss"
            ,"min_weight_constraint","max_weight_constraint","is_core_holding"
            ,"is_restricted"]