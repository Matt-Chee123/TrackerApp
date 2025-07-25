from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'security',views.SecurityViewSet)
router.register(r'pricehistory',views.PriceHistoryViewSet)

urlpatterns = [
    path('api/securities/', include(router.urls)),
]