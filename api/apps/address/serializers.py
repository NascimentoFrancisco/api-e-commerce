from rest_framework import serializers
from api.apps.address.models import Address
from api.apps.user.serializers import UserSerializer


class AddressSerializer(serializers.ModelSerializer):
    """Serializing class for the Address Model attributes"""

    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        """Meta class of this serializer"""

        model = Address
        ordering = ["created_at"]
        fields = [
            "id",
            "user",
            "cep",
            "city",
            "state",
            "district",
            "street",
            "number",
            "complement",
            "phone_number",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
