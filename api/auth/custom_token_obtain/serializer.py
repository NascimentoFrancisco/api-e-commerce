# pylint: disable=abstract-method
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom serializer to return user id along with tokens"""

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user_id"] = self.user.id
        return data
