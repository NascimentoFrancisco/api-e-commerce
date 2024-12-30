# pylint: disable=no-member
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.apps.shopping_cart.models import ShoppingCart
from api.apps.products.serializers import ProductSerializer
from api.apps.products.models import Product


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializing class for the ShoppingCart Model attributes"""

    id = serializers.UUIDField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.SerializerMethodField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        """Meta class of this serializer"""

        model = ShoppingCart
        ordering = ["created_at"]
        fields = ["id", "user", "product", "product_id", "status"]

    def get_product(self, obj):
        # Retorna a representação do produto usando o ProductSerializer
        return ProductSerializer(obj.product).data

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        try:
            return super().create(validated_data)
        except IntegrityError as exception:
            raise ValidationError(
                {"detail": "O produto já está no carrinho para este usuário."}
            ) from exception
