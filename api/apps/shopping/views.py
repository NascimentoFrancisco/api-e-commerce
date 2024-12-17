# pylint: disable=no-member
from rest_framework import viewsets
from api.apps.shopping.models import Shopping
from api.apps.shopping.serializers import ShoppingSerializer
from api.apps.shopping.permissions import IsAuthenticatedOrSuperUserForDelete


class ShoppingView(viewsets.ModelViewSet):
    """View class for the Shopping model"""

    queryset = Shopping.objects.all()
    serializer_class = ShoppingSerializer
    permission_classes = [IsAuthenticatedOrSuperUserForDelete]
