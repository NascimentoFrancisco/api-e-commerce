# Generated by Django 5.1.4 on 2025-01-09 19:23

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("cep", models.CharField(max_length=12, verbose_name="CEP")),
                ("city", models.CharField(max_length=255, verbose_name="Cidade")),
                ("state", models.CharField(max_length=255, verbose_name="Estado")),
                ("district", models.CharField(max_length=255, verbose_name="Bairro")),
                (
                    "street",
                    models.CharField(max_length=255, verbose_name="Rua/Avenida"),
                ),
                (
                    "number",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Deixar '0' caso não tenha número no endereço.",
                        verbose_name="Número",
                    ),
                ),
                (
                    "complement",
                    models.CharField(max_length=255, verbose_name="Rua/Avenida"),
                ),
                (
                    "phone_number",
                    models.CharField(max_length=11, verbose_name="Telefone"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "endereço",
                "verbose_name_plural": "endereços",
                "ordering": ["created_at"],
            },
        ),
    ]
