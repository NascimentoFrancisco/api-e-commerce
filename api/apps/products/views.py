# pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from api.apps.products.models import Product
from api.apps.products.serializers import ProductSerializer


class ProductView(viewsets.ModelViewSet):
    """View class for the Product model"""

    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Criação de um produto com upload de imagem.",
        consumes=["multipart/form-data"],
    )
    def create(self, request, *args, **kwargs):
        """POST - Cria um novo produto"""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Atualização de um produto com upload de imagem.",
        consumes=["multipart/form-data"],
    )
    def update(self, request, *args, **kwargs):
        """PUT - Atualiza um produto"""
        return super().update(request, *args, **kwargs)
