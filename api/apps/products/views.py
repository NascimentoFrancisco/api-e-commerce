# pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.apps.products.models import Product
from api.apps.products.serializers import ProductSerializer


class ProductView(viewsets.ModelViewSet):
    """View class for the Product model"""

    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
