from rest_framework import serializers
from api.apps.categories.models import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    """Serializing class for the Categories Model attributes"""

    id = serializers.UUIDField(read_only=True)
    slug = serializers.CharField(read_only=True)

    class Meta:
        """Meta class of this serializer"""

        model = Categories
        ordering = ["created_at"]
        fields = ["id", "title", "description", "slug", "status"]
