from django.db import models
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta


class Security(models.Model):
    """Main security definition"""

    symbol = models.CharField(max_length=20, unique=True, primary_key=True)
    isin = models.CharField(max_length=12, null=True, blank=True, unique=True)
    cusip = models.CharField(max_length=9, null=True, blank=True)
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50, null=True, blank=True)

    asset_class = models.CharField(max_length=20, choices=[
        ('EQUITY', 'Stock'),
        ('ETF', 'ETF'),
        ('BOND', 'Bond'),
        ('MUTUAL_FUND', 'Mutual Fund'),
        ('COMMODITY', 'Commodity'),
        ('CRYPTO', 'Cryptocurrency'),
        ('REIT', 'REIT'),
        ('INDEX', 'Index'),
        ('OPTION', 'Option'),
        ('FUTURE', 'Future'),
    ])

    security_type = models.CharField(max_length=30, null=True, blank=True)
    primary_exchange = models.CharField(max_length=10)
    currency = models.CharField(max_length=3, default='USD')
    country = models.CharField(max_length=2)

    sector = models.CharField(max_length=50, choices=[
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
    ], null=True, blank=True)

    industry = models.CharField(max_length=100, null=True, blank=True)
    sub_industry = models.CharField(max_length=100, null=True, blank=True)
    market_cap = models.BigIntegerField(null=True, blank=True)
    shares_outstanding = models.BigIntegerField(null=True, blank=True)

    # Bond fields
    maturity_date = models.DateField(null=True, blank=True)
    coupon_rate = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    credit_rating = models.CharField(max_length=10, null=True, blank=True)

    # Fund fields
    expense_ratio = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    fund_family = models.CharField(max_length=100, null=True, blank=True)

    # Trading info
    is_actively_traded = models.BooleanField(default=True)
    average_volume = models.BigIntegerField(null=True, blank=True)
    last_price = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    price_updated_at = models.DateTimeField(null=True, blank=True)

    data_source = models.CharField(max_length=50, default='yfinance')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['asset_class', 'sector']),
            models.Index(fields=['currency', 'country']),
            models.Index(fields=['is_actively_traded']),
        ]
        db_table = "security"


    def __str__(self):
        return f"{self.symbol} - {self.name}"


class MarketSnapshot(models.Model):
    """Current market data"""

    security = models.OneToOneField(Security, on_delete=models.CASCADE, related_name='current_market_data')

    last_price = models.DecimalField(max_digits=18, decimal_places=6)
    bid_price = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    ask_price = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    bid_size = models.BigIntegerField(null=True, blank=True)
    ask_size = models.BigIntegerField(null=True, blank=True)

    open_price = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    high_price = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    low_price = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    previous_close = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)

    volume = models.BigIntegerField(default=0)
    avg_volume_10d = models.BigIntegerField(null=True, blank=True)
    avg_volume_30d = models.BigIntegerField(null=True, blank=True)

    change_amount = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    change_percent = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    market_timestamp = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.security.symbol} - ${self.last_price}"


class PriceHistory(models.Model):
    """Historical OHLCV data"""

    security = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='price_history')
    date = models.DateField()

    open_price = models.DecimalField(max_digits=18, decimal_places=6)
    high_price = models.DecimalField(max_digits=18, decimal_places=6)
    low_price = models.DecimalField(max_digits=18, decimal_places=6)
    close_price = models.DecimalField(max_digits=18, decimal_places=6)
    adjusted_close = models.DecimalField(max_digits=18, decimal_places=6)
    volume = models.BigIntegerField()

    dividend_amount = models.DecimalField(max_digits=12, decimal_places=6, default=Decimal('0'))
    split_ratio = models.DecimalField(max_digits=10, decimal_places=6, default=Decimal('1.0'))

    return_1d = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ['security', 'date']
        indexes = [
            models.Index(fields=['security', 'date']),
            models.Index(fields=['date']),
        ]
        ordering = ['-date']

    def __str__(self):
        return f"{self.security.symbol} - {self.date}"


class RiskMetrics(models.Model):
    """Risk and performance metrics"""

    security = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='risk_metrics')
    calculation_date = models.DateField()
    lookback_period = models.IntegerField()

    volatility_annualized = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    sharpe_ratio = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    sortino_ratio = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    max_drawdown = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    var_95 = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    var_99 = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

    beta = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    alpha = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    correlation_market = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)

    total_return = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    annualized_return = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['security', 'calculation_date', 'lookback_period']
        indexes = [
            models.Index(fields=['security', 'calculation_date']),
            models.Index(fields=['sharpe_ratio']),
        ]

    def __str__(self):
        return f"{self.security.symbol} Risk ({self.lookback_period}d)"


class TechnicalIndicators(models.Model):
    """Technical analysis indicators"""

    security = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='technical_indicators')
    date = models.DateField()

    sma_20 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    sma_50 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    sma_200 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    ema_12 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    ema_26 = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)

    rsi_14 = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    macd_line = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)
    macd_signal = models.DecimalField(max_digits=12, decimal_places=6, null=True, blank=True)

    bb_upper = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    bb_middle = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    bb_lower = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)

    support_level = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    resistance_level = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)

    class Meta:
        unique_together = ['security', 'date']
        indexes = [
            models.Index(fields=['security', 'date']),
        ]
        ordering = ['-date']

    def __str__(self):
        return f"{self.security.symbol} Technical - {self.date}"


class SecurityCorrelation(models.Model):
    """Pairwise correlations between securities"""

    security_1 = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='correlations_as_first')
    security_2 = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='correlations_as_second')
    calculation_date = models.DateField()
    lookback_period = models.IntegerField()

    price_correlation = models.DecimalField(max_digits=6, decimal_places=4)
    return_correlation = models.DecimalField(max_digits=6, decimal_places=4, null=True, blank=True)
    return_covariance = models.DecimalField(max_digits=15, decimal_places=8, null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['security_1', 'security_2', 'calculation_date', 'lookback_period']
        indexes = [
            models.Index(fields=['security_1', 'security_2']),
        ]

    def __str__(self):
        return f"{self.security_1.symbol} vs {self.security_2.symbol}"


class TradingSignal(models.Model):
    """Trading signals and recommendations"""

    SIGNAL_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('HOLD', 'Hold'),
        ('REDUCE', 'Reduce Position'),
        ('INCREASE', 'Increase Position'),
    ]

    SIGNAL_SOURCES = [
        ('MOMENTUM', 'Momentum Strategy'),
        ('MEAN_REVERSION', 'Mean Reversion'),
        ('TECHNICAL', 'Technical Analysis'),
        ('FUNDAMENTAL', 'Fundamental Analysis'),
        ('RISK_MANAGEMENT', 'Risk Management'),
        ('PORTFOLIO_REBALANCE', 'Portfolio Rebalancing'),
    ]

    security = models.ForeignKey(Security, on_delete=models.CASCADE, related_name='trading_signals')
    signal_type = models.CharField(max_length=20, choices=SIGNAL_TYPES)
    signal_source = models.CharField(max_length=30, choices=SIGNAL_SOURCES)

    strength = models.DecimalField(max_digits=4, decimal_places=2)  # 0-100 confidence
    target_price = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    stop_loss = models.DecimalField(max_digits=18, decimal_places=6, null=True, blank=True)
    time_horizon = models.IntegerField(null=True, blank=True)  # Days

    risk_level = models.CharField(max_length=10, choices=[
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ], default='MEDIUM')

    reasoning = models.TextField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['security', 'is_active']),
            models.Index(fields=['signal_type', 'is_active']),
            models.Index(fields=['created_at']),
            models.Index(fields=['strength']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.security.symbol} - {self.signal_type} ({self.strength}%)"


class MarketRegime(models.Model):
    """Market regime classification"""

    REGIME_TYPES = [
        ('BULL', 'Bull Market'),
        ('BEAR', 'Bear Market'),
        ('SIDEWAYS', 'Sideways/Range-bound'),
        ('HIGH_VOLATILITY', 'High Volatility'),
        ('LOW_VOLATILITY', 'Low Volatility'),
    ]

    date = models.DateField(unique=True)
    regime_type = models.CharField(max_length=20, choices=REGIME_TYPES)

    vix_level = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    market_trend = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    volatility_regime = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)

    confidence = models.DecimalField(max_digits=4, decimal_places=2)  # 0-100
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - {self.regime_type}"