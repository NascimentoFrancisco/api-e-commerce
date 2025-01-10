# pylint:disable=no-member
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.apps.shopping_cart.models import ShoppingCart
from api.apps.products.serializers import ProductSerializer


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializing class for the ShoppingCart Model attributes"""

    id = serializers.UUIDField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        """Meta class of this serializer"""

        model = ShoppingCart
        ordering = ["created_at"]
        fields = ["id", "user", "product", "status"]


class ShoppingCartCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer only for creating and editing"""

    class Meta:
        """Meta class of this serializer"""

        model = ShoppingCart
        fields = ["product", "status"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        try:
            return super().create(validated_data)
        except IntegrityError as exception:
            raise ValidationError(
                {"detail": "O produto já está no carrinho para este usuário."}
            ) from exception
