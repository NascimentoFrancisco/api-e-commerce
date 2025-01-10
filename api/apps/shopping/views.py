# pylint: disable=no-member
from rest_framework import viewsets
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from api.apps.shopping.models import Shopping
from api.apps.products.models import Product
from api.apps.shopping.serializers import (
    ShoppingSerializer,
    ShoppingCreateUpdateSerializer,
)
from api.apps.shopping.permissions import IsAuthenticatedOrSuperUserForDelete


class ShoppingView(viewsets.ModelViewSet):
    """View class for the Shopping model"""

    queryset = Shopping.objects.all()
    permission_classes = [IsAuthenticatedOrSuperUserForDelete]
    filter_backends = [SearchFilter]
    search_fields = ["user__id"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ShoppingCreateUpdateSerializer
        return ShoppingSerializer

    @swagger_auto_schema(
        request_body=ShoppingCreateUpdateSerializer, responses={201: ShoppingSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # Garantir que perform_create seja chamado
        response_serializer = ShoppingSerializer(serializer.instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ShoppingCreateUpdateSerializer, responses={200: ShoppingSerializer}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_serializer = ShoppingSerializer(instance)
        return Response(response_serializer.data)

    @swagger_auto_schema(
        request_body=ShoppingCreateUpdateSerializer, responses={200: ShoppingSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response_serializer = ShoppingSerializer(instance)
        return Response(response_serializer.data)

    def perform_create(self, serializer):
        product: Product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity_products"]

        if product.amount < quantity:
            raise ValidationError(
                {"detail": "A quantidade solicitada excede o estoque disponível."}
            )
        product.amount -= quantity
        product.save()

        return serializer.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        product: Product = serializer.validated_data.get("product", instance.product)
        new_quantity = serializer.validated_data.get(
            "quantity_products", instance.quantity_products
        )

        old_quantity = instance.quantity_products

        if new_quantity > product.amount + old_quantity:
            raise ValidationError(
                {"detail": "A quantidade solicitada excede o estoque disponível."}
            )

        product.amount += old_quantity
        product.amount -= new_quantity
        product.save()

        serializer.save()

    def perform_destroy(self, instance):
        instance = self.get_object()
        product: Product = instance.product

        product.amount += instance.quantity_products
        product.save()

        return super().perform_destroy(instance)
