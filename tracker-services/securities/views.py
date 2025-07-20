from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Security, PriceHistory
from .serializers import SecuritySerializer, PriceHistorySerializer

class SecurityViewSet(viewsets.ModelViewSet):
    queryset = Security.objects.all()
    serializer_class = SecuritySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['symbol']


class PriceHistoryViewSet(viewsets.ModelViewSet):
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['security']
    ordering_fields = ['date']
    ordering = ['-date']




