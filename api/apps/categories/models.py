import uuid
from django.db import models
from django.utils.text import slugify


class Categories(models.Model):
    """Category model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    slug = models.SlugField(unique=True)
    status = models.BooleanField(verbose_name="Ativa ou não ativa", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Categories, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        """Meta Class"""

        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
