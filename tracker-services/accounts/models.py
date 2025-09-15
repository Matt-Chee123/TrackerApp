# portfolio/models.py
from django.db import models
from django.conf import settings
from securities.models import Security


class Portfolio(models.Model):
    name = models.CharField(max_length=80)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=20, decimal_places=4, default=0)

    last_rebalance_date = models.DateTimeField(null=True, blank=True)
    drift_threshold = models.DecimalField(max_digits=5, decimal_places=4, default=0.05)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "portfolio"

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Holding(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='holdings')
    security = models.ForeignKey(Security, on_delete=models.CASCADE)

    quantity = models.DecimalField(max_digits=15, decimal_places=6)
    average_cost = models.DecimalField(max_digits=15, decimal_places=4)

    target_weight = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    min_weight_constraint = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)
    max_weight_constraint = models.DecimalField(max_digits=5, decimal_places=4, null=True, blank=True)

    state = models.CharField(max_length=10, default='active')
    is_core_holding = models.BooleanField(default=False)
    is_restricted = models.BooleanField(default=False)
    last_rebalance_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "holdings"
        unique_together = ('portfolio', 'security')

    def __str__(self):
        return f"{self.security.symbol} ({self.quantity} shares)"


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
        ('deposit', 'Cash Deposit'),
        ('withdrawal', 'Cash Withdrawal'),
        ('dividend', 'Dividend'),
        ('fee', 'Fee'),
        ('interest', 'Interest'),
    ]

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, null=True, blank=True, related_name='transactions')

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=15, decimal_places=6, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    description = models.TextField(blank=True)
    transaction_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
        ordering = ['-transaction_date']

    def __str__(self):
        return f"{self.transaction_type.upper()} {self.quantity or ''} {self.holding.security.symbol if self.holding else 'CASH'}"


class Lot(models.Model):
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name='lots')
    quantity = models.DecimalField(max_digits=10, decimal_places=6)
    remaining_quantity = models.DecimalField(max_digits=10, decimal_places=6)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField()
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_closed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lots"
        ordering = ['purchase_date']

    def __str__(self):
        return f"Lot: {self.remaining_quantity}/{self.quantity} {self.holding.security.symbol} @ ${self.purchase_price}"


class PortfolioSnapshot(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='snapshots')
    date = models.DateField()
    total_value = models.DecimalField(max_digits=20, decimal_places=2)
    cash_balance = models.DecimalField(max_digits=20, decimal_places=4)
    securities_value = models.DecimalField(max_digits=20, decimal_places=2)
    daily_return = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "portfolio_snapshots"
        unique_together = ('portfolio', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.portfolio.name} snapshot {self.date}"