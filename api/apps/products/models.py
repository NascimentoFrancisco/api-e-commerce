import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from api.apps.categories.models import Categories


class Product(models.Model):
    """Product model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    description = models.TextField(blank=False, null=False)
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, null=False, blank=False
    )
    amount = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=24, decimal_places=2)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(default=True)
    image_url = models.URLField(max_length=2048, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(Product, self).save(*args, **kwargs)

    def __str__(self) -> None:
        return f"{self.name}"

    class Meta:
        """Meta class"""

        ordering = ["created_at"]
        verbose_name = "produto"
        verbose_name_plural = "produtos"
