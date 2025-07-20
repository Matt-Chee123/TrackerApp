from django.db import models
from django.conf import settings

SECTOR_CHOICES = [
    ('ENERGY', 'Energy'),
    ('MATERIALS', 'Materials'),
    ('INDUSTRIALS', 'Industrials'),
    ('CONSUMER_DISCRETIONARY', 'Consumer Discretionary'),
    ('CONSUMER_STAPLES', 'Consumer Staples'),
    ('HEALTHCARE', 'Healthcare'),
    ('FINANCIALS', 'Financials'),
    ('INFORMATION_TECHNOLOGY', 'Information Technology'),
    ('COMMUNICATION_SERVICES', 'Communication Services'),
    ('UTILITIES', 'Utilities'),
    ('REAL_ESTATE', 'Real Estate'),
]


class Security(models.Model):
    symbol = models.CharField(max_length=20, unique=True, primary_key=True)
    isin = models.CharField(max_length=12, null=True, blank=True, unique=True)
    cusip = models.CharField(max_length=9, null=True, blank=True)
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, null=True, blank=True)
    asset_class = models.CharField(max_length=20, choices=[
        ('EQUITY', 'Stock'),
        ('BOND', 'Bond'),
        ('ETF', 'Exchange Traded Fund'),
        ('MUTUAL_FUND', 'Mutual Fund'),
        ('COMMODITY', 'Commodity'),
        ('CRYPTO', 'Cryptocurrency'),
        ('REIT', 'Real Estate Investment Trust'),
        ('INDEX', 'Index'),
    ])
    security_type = models.CharField(max_length=30, null=True, blank=True)
    primary_exchange = models.CharField(max_length=10)
    currency = models.CharField(max_length=3, default='USD')
    country = models.CharField(max_length=2)  # ISO country code
    sector = models.CharField(max_length=50, choices=SECTOR_CHOICES, null=True, blank=True)
    industry = models.CharField(max_length=100, null=True, blank=True)
    sub_industry = models.CharField(max_length=100, null=True, blank=True)
    market_cap = models.BigIntegerField(null=True, blank=True)
    shares_outstanding = models.BigIntegerField(null=True, blank=True)
    maturity_date = models.DateField(null=True, blank=True)
    coupon_rate = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    credit_rating = models.CharField(max_length=10, null=True, blank=True)
    expense_ratio = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    fund_family = models.CharField(max_length=100, null=True, blank=True)
    last_price = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    price_updated_at = models.DateTimeField(null=True, blank=True)
    average_volume = models.BigIntegerField(null=True, blank=True)
    is_actively_traded = models.BooleanField(default=True)
    data_source = models.CharField(max_length=50, default='yfinance')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['sector', 'asset_class']),
            models.Index(fields=['currency', 'country']),
            models.Index(fields=['price_updated_at']),
        ]
        db_table = "security"


class PriceHistory(models.Model):
    security = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='prices')

    date = models.DateField()

    open_price = models.DecimalField(max_digits=15, decimal_places=4)
    high_price = models.DecimalField(max_digits=15, decimal_places=4)
    low_price = models.DecimalField(max_digits=15, decimal_places=4)
    close_price = models.DecimalField(max_digits=15, decimal_places=4)

    adjusted_close = models.DecimalField(max_digits=15, decimal_places=4)
    volume = models.BigIntegerField()
    dividend_amount = models.DecimalField(max_digits=10, decimal_places=4, default=0)

    split_ratio = models.DecimalField(max_digits=10, decimal_places=6, default=1.0)

    class Meta:
        unique_together = ['security', 'date']
        indexes = [
            models.Index(fields=['security', 'date']),
            models.Index(fields=['date']),
        ]