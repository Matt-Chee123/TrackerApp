from django.db import models
from django.conf import settings
from securities.models import Security

class Account(models.Model):
    account_name = models.CharField(max_length=80)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_market_value = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    cash_balance = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    net_worth = models.DecimalField(max_digits=20, decimal_places=4, null=True, blank=True)
    unrealized_gain_loss = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unrealized_gain_loss_pct = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    last_rebalance_date = models.DateTimeField(null=True, blank=True)
    drift_threshold = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)

    class Meta:
        db_table = "portfolio"


class Holdings(models.Model):
    name = models.CharField(max_length=80)
    code = models.ForeignKey(Security, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    state = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=15, decimal_places=6)
    current_price = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    target_weight = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    actual_weight = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    last_rebalance_date = models.DateTimeField(null=True, blank=True)
    average_cost = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    total_cost_basis = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unrealized_gain_loss = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unrealized_gain_loss_pct = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    min_weight_constraint = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    max_weight_constraint = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    is_core_holding = models.BooleanField(default=False)
    is_restricted = models.BooleanField(default=False)

    class Meta:
        db_table = "holdings"


class Transactions(models.Model):
    TRANSACTION_TYPE = [
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ]
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Changed from portfolio
    holding = models.ForeignKey(Holdings, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE)
    quantity = models.DecimalField(max_digits=15, decimal_places=6)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"


class Lots(models.Model):
    holding = models.ForeignKey(Holdings, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=6)
    remaining_quantity = models.DecimalField(max_digits=10, decimal_places=6)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    is_closed = models.BooleanField(default=False)

    class Meta:
        db_table = "lots"
