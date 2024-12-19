from django.core import exceptions
from django.contrib.auth import password_validation
from rest_framework import serializers
from api.apps.user.models import User


class UserSerializer(serializers.ModelSerializer):
    """User model serializer class"""

    id = serializers.UUIDField(read_only=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Meta class of this serializer"""

        model = User
        ordering = ["created_at"]
        fields = [
            "id",
            "name",
            "username",
            "email",
            "is_superuser",
            "password1",
            "password2",
        ]

    def validate(self, attrs) -> None:
        password1 = attrs.get("password1")
        password2 = attrs.get("password2")

        if password1 != password2:
            raise serializers.ValidationError({"password1": "Senhas diferentes"})

        user = User(
            name=attrs.get("name"),
            username=attrs.get("username"),
            email=attrs.get("email"),
        )
        try:
            password_validation.validate_password(password=password1, user=user)
        except exceptions.ValidationError as exception:
            raise serializers.ValidationError({"password1": list(exception)})

        return super(UserSerializer, self).validate(attrs)

    def create(self, validated_data) -> User:
        password = validated_data.pop("password1")
        user = User(
            name=validated_data.pop("name"),
            username=validated_data.pop("username"),
            email=validated_data.pop("email"),
        )
        user.is_active = True
        user.is_superuser = False
        user.set_password(password)
        user.save()

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    """Dedicated serializer only for user data update"""

    id = serializers.UUIDField(read_only=True)

    class Meta:
        """Meta class of this serializer"""

        model = User
        fields = ["id", "name", "username", "email"]
