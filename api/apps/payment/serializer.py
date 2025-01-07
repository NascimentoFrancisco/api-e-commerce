from rest_framework import serializers
from api.apps.payment.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serializing class for the Payment Model attributes"""

    id = serializers.UUIDField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        "Meta class of the serializer"

        model = Payment
        fields = [
            "id",
            "user",
            "shopping",
            "payment_method",
            "divided_into",
            "slug",
            "value",
            "total_value",
            "created_at",
            "updated_at",
        ]
        ordering = ["created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
