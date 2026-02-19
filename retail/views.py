from rest_framework import viewsets

from retail.models import Retail, Product
from retail.serializers import RetailSerializer, ProductSerializer


class RetailViewSet(viewsets.ModelViewSet):
    serializer_class = RetailSerializer
    queryset = Retail.objects.all()

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()