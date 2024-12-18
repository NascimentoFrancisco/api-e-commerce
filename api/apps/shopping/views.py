# pylint: disable=no-member
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from api.apps.shopping.models import Shopping
from api.apps.products.models import Product
from api.apps.shopping.serializers import ShoppingSerializer
from api.apps.shopping.permissions import IsAuthenticatedOrSuperUserForDelete


class ShoppingView(viewsets.ModelViewSet):
    """View class for the Shopping model"""

    queryset = Shopping.objects.all()
    serializer_class = ShoppingSerializer
    permission_classes = [IsAuthenticatedOrSuperUserForDelete]

    def perform_create(self, serializer):
        product: Product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity_products"]

        if product.amount < quantity:
            raise ValidationError(
                {"detail": "A quantidade solicitada excede o estoque disponível."}
            )
        product.amount -= quantity
        product.save()

        return serializer.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        product: Product = serializer.validated_data.get("product", instance.product)
        new_quantity = serializer.validated_data.get(
            "quantity_products", instance.quantity_products
        )

        old_quantity = instance.quantity_products

        if new_quantity > product.amount + old_quantity:
            raise ValidationError(
                {"detail": "A quantidade solicitada excede o estoque disponível."}
            )

        product.amount += old_quantity
        product.amount -= new_quantity
        product.save()

        serializer.save()

    def perform_destroy(self, instance):
        instance = self.get_object()
        product: Product = instance.product

        product.amount += instance.quantity_products
        product.save()

        return super().perform_destroy(instance)
