# pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema
from api.apps.products.models import Product
from api.apps.products.serializers import ProductSerializer
from api.apps.products.permissions import IsAuthenticatedAndSuperUserForUnsafeMethods


class ProductView(viewsets.ModelViewSet):
    """View class for the Product model"""

    permission_classes = [IsAuthenticatedAndSuperUserForUnsafeMethods]
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [SearchFilter]

    search_fields = ["category__title", "category__slug", "name", "slug"]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            return Product.objects.filter(user=user)
        return Product.objects.filter(status=True)

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
