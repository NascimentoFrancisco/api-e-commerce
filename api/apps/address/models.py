import uuid
from django.db import models
from django.conf import settings


class Address(models.Model):
    """Addres Model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cep = models.CharField(verbose_name="CEP", max_length=12, blank=False, null=False)
    city = models.CharField(
        verbose_name="Cidade", max_length=255, blank=False, null=False
    )
    state = models.CharField(
        verbose_name="Estado", max_length=255, blank=False, null=False
    )
    district = models.CharField(
        verbose_name="Bairro", max_length=255, blank=False, null=False
    )
    street = models.CharField(
        verbose_name="Rua/Avenida", max_length=255, blank=False, null=False
    )
    number = models.PositiveIntegerField(
        verbose_name="Número",
        default=0,
        help_text="Deixar '0' caso não tenha número no endereço.",
    )
    complement = models.CharField(
        verbose_name="Rua/Avenida", max_length=255, blank=False, null=False
    )
    phone_number = models.CharField(
        verbose_name="Telefone", max_length=11, blank=False, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.city}"

    class Meta:
        """Meta class"""

        ordering = ["created_at"]
        verbose_name = "endereço"
        verbose_name_plural = "endereços"
