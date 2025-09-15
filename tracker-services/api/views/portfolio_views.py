from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import Portfolio, Holding
from securities.models import Security
from api.serializers import PortfolioSerializer, HoldingSerializer
from core.services.portfolio_service import PortfolioService

class PortfolioListCreateView(generics.ListCreateAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer

class PortfolioDetailView(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer


@api_view(['POST'])
def add_holding(request, portfolio_id):
    try:
        portfolio = Portfolio.objects.get(id=portfolio_id)
        security = Security.objects.get(symbol=request.data['symbol'])
        quantity = request.data['quantity']
        avg_price = request.data['average_price']

        Holding.objects.create(
            portfolio=portfolio,
            security=security,
            quantity=quantity,
            average_price=avg_price
        )
        return Response({'message': 'Holding added successfully'})
    except Portfolio.DoesNotExist:
        return Response({'error': 'Portfolio not found'}, status=status.HTTP_404_NOT_FOUND)
    except Security.DoesNotExist:
        return Response({'error': 'Security not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def portfolio_value(request, portfolio_id):
    service = PortfolioService()
    total_value = service.get_portfolio_value(portfolio_id)
    return Response({'portfolio_id': portfolio_id, 'total_value': total_value})

@api_view(['GET'])
def portfolio_holdings(request, portfolio_id):
    service = PortfolioService()
    holdings = service.get_portfolio_holdings(portfolio_id)
    return Response({'portfolio_id': portfolio_id, 'holdings': holdings})
