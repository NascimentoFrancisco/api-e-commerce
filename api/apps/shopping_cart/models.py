import uuid
from django.db import models
from django.conf import settings
from api.apps.products.models import Product


class ShoppingCart(models.Model):
    """ShoppingCart Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False
    )
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> None:
        return f"{self.product.name}"

    class Meta:
        """Meta class"""

        ordering = ["created_at"]
        verbose_name = "Carrinho"
        verbose_name_plural = "carrinhos"
        unique_together = ["user", "product"]
