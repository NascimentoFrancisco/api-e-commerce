# pylint: disable=no-member
from rest_framework import serializers
from api.apps.shopping.models import Shopping
from api.apps.products.serializers import ProductSerializer
from api.apps.address.serializers import AddressSerializer


class ShoppingSerializer(serializers.ModelSerializer):
    """Serializing class for the Shopping Model attributes"""

    id = serializers.UUIDField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    product = ProductSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        """Meta class of this serializer"""

        model = Shopping
        ordering = ["created_at"]
        fields = [
            "id",
            "slug",
            "user",
            "product",
            "quantity_products",
            "status",
            "cancelled",
            "payment_status",
            "address",
            "created_at",
            "updated_at",
        ]


class ShoppingCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer only for creating and editing Malls"""

    class Meta:
        """Meta class of this serializer"""

        model = Shopping
        fields = [
            "product",
            "quantity_products",
            "status",
            "cancelled",
            "payment_status",
            "address",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
