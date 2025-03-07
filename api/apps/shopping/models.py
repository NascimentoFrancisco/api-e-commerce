import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from api.apps.products.models import Product
from api.apps.address.models import Address


class Shopping(models.Model):
    """Shopping Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, blank=False
    )
    slug = models.SlugField("slug", unique=True, db_index=True)
    quantity_products = models.PositiveIntegerField(
        verbose_name="Quantidade de produtos", default=0
    )
    value = models.DecimalField(
        verbose_name="Valor da compra", max_digits=24, decimal_places=2, default=0
    )
    shipping_value = models.DecimalField(
        verbose_name="Valor do frete", max_digits=24, decimal_places=2, default=0
    )
    status = models.BooleanField(verbose_name="Finalizada ou em aberto", default=True)
    cancelled = models.BooleanField(verbose_name="Cancelada ou não", default=False)
    payment_status = models.BooleanField(
        verbose_name="Pagamento pendente ou finalizado", default=False
    )
    address = models.ForeignKey(
        Address,
        verbose_name="Endereço",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.product.name} {self.user.name}")
        super(Shopping, self).save(*args, **kwargs)

    def __str__(self) -> None:
        return f"{self.product.name}"

    class Meta:
        """Meta class"""

        ordering = ["created_at"]
        verbose_name = "Compra"
        verbose_name_plural = "compras"
