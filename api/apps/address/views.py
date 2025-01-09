# pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from api.apps.address.models import Address
from api.apps.address.serializers import AddressSerializer


class AddressView(viewsets.ModelViewSet):
    """View class of the Address"""

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["user__id"]
