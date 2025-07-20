from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'accounts',views.AccountViewSet)
router.register(r'transactions',views.TransactionsViewSet)
router.register(r'holdings',views.HoldingsViewSet)

urlpatterns = [
    path('api/accounts/', include(router.urls)),
]