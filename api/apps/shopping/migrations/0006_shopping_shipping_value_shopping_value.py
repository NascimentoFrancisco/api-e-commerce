# Generated by Django 5.1.4 on 2025-01-16 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopping", "0005_shopping_address"),
    ]

    operations = [
        migrations.AddField(
            model_name="shopping",
            name="shipping_value",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=24,
                verbose_name="Valor do frete",
            ),
        ),
        migrations.AddField(
            model_name="shopping",
            name="value",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=24,
                verbose_name="Valor da compra",
            ),
        ),
    ]
