# pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.apps.shopping_cart.models import ShoppingCart
from api.apps.shopping_cart.serializers import ShoppingCartSerializer


class ShoppingCartView(viewsets.ModelViewSet):
    """View class for the ShoppingCart model"""

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]
