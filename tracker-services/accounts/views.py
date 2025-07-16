from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Account, Holdings, Transactions
from .serializers import AccountSerializer, HoldingsSerializer, TransactionsSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user','account_name']
    ordering_fields = ['created_date']
    ordering = ['-created_date']

class HoldingsViewSet(viewsets.ModelViewSet):
    queryset = Holdings.objects.all()
    serializer_class = HoldingsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account']

class TransactionsViewSet(viewsets.ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'transaction_type']


