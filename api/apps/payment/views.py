# pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from api.apps.payment.serializer import PaymentSerializer
from api.apps.payment.models import Payment


class PyamentView(viewsets.ModelViewSet):
    """View class for Pyament model"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["user__id", "shopping_id"]
