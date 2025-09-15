from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'accounts',views.PortfolioViewSet)
router.register(r'transactions',views.TransactionViewSet)
router.register(r'holdings',views.HoldingViewSet)

urlpatterns = [
    path('api/accounts/', include(router.urls)),
]