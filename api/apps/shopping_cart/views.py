# pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from api.apps.shopping_cart.models import ShoppingCart
from api.apps.shopping_cart.serializers import (
    ShoppingCartSerializer,
    ShoppingCartCreateUpdateSerializer,
)


class ShoppingCartView(viewsets.ModelViewSet):
    """View class for the ShoppingCart model"""

    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ["user__id"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ShoppingCartCreateUpdateSerializer
        return ShoppingCartSerializer

    @swagger_auto_schema(
        request_body=ShoppingCartCreateUpdateSerializer,
        responses={201: ShoppingCartSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        response_serializer = ShoppingCartSerializer(instance)
        return Response(response_serializer.data, status=201, headers=headers)

    @swagger_auto_schema(
        request_body=ShoppingCartCreateUpdateSerializer,
        responses={200: ShoppingCartSerializer},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = ShoppingCartSerializer(instance)
        return Response(response_serializer.data)

    @swagger_auto_schema(
        request_body=ShoppingCartCreateUpdateSerializer,
        responses={200: ShoppingCartSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = ShoppingCartSerializer(instance)
        return Response(response_serializer.data)
