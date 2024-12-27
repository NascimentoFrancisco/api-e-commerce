from io import BytesIO
from django.core import exceptions
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers
from api.apps.products.models import Product
from api.apps.user.serializers import UserSerializer
from api.services.firebase.storage import HandleFirebaseStorage


class ProductSerializer(serializers.ModelSerializer):
    """Serializing class for the Product Model attributes"""

    id = serializers.UUIDField(read_only=True)
    user = UserSerializer(read_only=True)
    slug = serializers.SlugField(read_only=True)
    image = serializers.ImageField(write_only=True, required=True)
    image_url = serializers.URLField(read_only=True)

    class Meta:
        """Meta class of this serializer"""

        model = Product
        ordering = ["created_at"]
        fields = [
            "id",
            "name",
            "user",
            "description",
            "category",
            "amount",
            "price",
            "slug",
            "status",
            "image",
            "image_url",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user

        image: InMemoryUploadedFile = validated_data.pop("image")
        name: str = validated_data["name"]
        image_name_to_save = slugify(name)

        try:
            handle_firebase_storage = HandleFirebaseStorage()
            public_url = handle_firebase_storage.upload_image_to_storage(
                image.file, image_name_to_save, image.content_type
            )
            validated_data["image_url"] = public_url
        except Exception as exception:
            raise exceptions.BadRequest({"image": exception.args})

        return super().create(validated_data)

    def update(self, instance: Product, validated_data):
        image: InMemoryUploadedFile = validated_data.pop("image", None)
        handle_firebase_storage = HandleFirebaseStorage()

        if image:
            if instance.image_url:
                previous_image_path = instance.image_url.split(".com")[-1]
                try:
                    handle_firebase_storage.delete_blob(previous_image_path[1:])
                except Exception as exception:
                    raise exceptions.BadRequest({"image": exception.args})

            try:
                image_name_to_save = slugify(instance.name)
                public_url = handle_firebase_storage.update_image_in_storage(
                    BytesIO(image.read()), image_name_to_save, image.content_type
                )
                validated_data["image_url"] = public_url
            except Exception as exception:
                raise exceptions.BadRequest({"image": exception.args})

        return super().update(instance, validated_data)
