from django.db import models
from django.conf import settings

class Account(models.Model):
    account_name = models.CharField(max_length=30)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = "user_account"

class Holdings(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    state = models.CharField(max_length=10)
    quantity = models.DecimalField(max_digits=15, decimal_places=6)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "holdings"

class Transactions(models.Model):
    TRANSACTION_TYPE = [
        ('buy', 'Buy'),
        ('sell', 'Sell')
    ]
    portfolio = models.ForeignKey(Account, on_delete=models.CASCADE)
    holding = models.ForeignKey(Holdings, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE)
    quantity = models.DecimalField(max_digits=15, decimal_places=6)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_date = models.DateTimeField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"