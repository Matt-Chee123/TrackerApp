# api/urls.py
from django.urls import path
from api.views.portfolio_views import (
    PortfolioListCreateView,
    PortfolioDetailView,
    add_holding,
    portfolio_value,
    portfolio_holdings
)


urlpatterns = [
    path('portfolios/', PortfolioListCreateView.as_view(), name='portfolio-list-create'),
    path('portfolios/<int:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('portfolios/<int:portfolio_id>/add-holding/', add_holding, name='add-holding'),
    path('portfolios/<int:portfolio_id>/value/', portfolio_value, name='portfolio-value'),
    path('portfolios/<int:portfolio_id>/holdings/', portfolio_holdings, name='portfolio-holdings'),
]
