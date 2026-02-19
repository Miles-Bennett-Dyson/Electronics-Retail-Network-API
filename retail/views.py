from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from retail.filters import CountryFilter
from retail.models import Retail, Product
from retail.serializers import RetailSerializer, ProductSerializer

class RetailViewSet(viewsets.ModelViewSet):
    serializer_class = RetailSerializer
    queryset = Retail.objects.all()
    filter_backends = [DjangoFilterBackend,]
    filterset_class = CountryFilter

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()