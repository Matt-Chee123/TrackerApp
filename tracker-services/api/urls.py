# api/urls.py
from django.urls import path
from api.views.portfolio_views import (
    PortfolioListCreateView,
    PortfolioDetailView,
    add_holding,
    portfolio_value
)

urlpatterns = [
    path('portfolios/', PortfolioListCreateView.as_view(), name='portfolio-list-create'),
    path('portfolios/<int:pk>/', PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('portfolios/<int:portfolio_id>/holdings/', add_holding, name='add-holding'),
    path('portfolios/<int:portfolio_id>/value/', portfolio_value, name='portfolio-value'),
]
