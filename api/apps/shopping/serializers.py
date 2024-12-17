# pylint: disable=no-member
from rest_framework import serializers
from api.apps.shopping.models import Shopping
from api.apps.products.models import Product
from api.apps.products.serializers import ProductSerializer


class ShoppingSerializer(serializers.ModelSerializer):
    """Serializing class for the Shopping Model attributes"""

    id = serializers.UUIDField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
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
            "product_id",
            "quantity_products",
            "status",
            "payment_status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
