import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from api.apps.shopping.models import Shopping


class PaymentMethods(models.TextChoices):
    """Helper class for choosing payment methods"""

    CREDIT_CARD = "CTC", "credit_card"
    BANK_SLIP = "BKS", "bank_slip"
    PIX = "PIX", "pix"


class Payment(models.Model):
    """Payment model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Usuário que cadstrou",
        on_delete=models.PROTECT,
    )
    shopping = models.ForeignKey(
        Shopping,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Categoria a qual o produto pertence",
    )
    payment_method = models.CharField(
        max_length=3,
        choices=PaymentMethods.choices,
        db_default=PaymentMethods.PIX,
        verbose_name="Forma de pagamento",
        help_text="Devem ser CTC = Cartão de crédito, BKS = Boleto bancário ou PIX = Pix",
    )
    divided_into = models.PositiveIntegerField(
        verbose_name="Dividido em quantas vezes", default=1
    )
    value = models.DecimalField(
        verbose_name="Valor parcial", max_digits=24, decimal_places=2
    )
    total_value = models.DecimalField(
        verbose_name="Valor total", max_digits=24, decimal_places=2
    )
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.name)
        return super(Payment, self).save(*args, **kwargs)

    def __str__(self) -> None:
        return f"{self.user.name}"

    class Meta:
        """Meta class"""

        ordering = ["created_at"]
        verbose_name = "pagamento"
        verbose_name_plural = "pagamentos"
