# Generated by Django 5.1.4 on 2024-12-29 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0002_categories_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="categories",
            name="status",
            field=models.BooleanField(default=True, verbose_name="Ativa ou não ativa"),
        ),
    ]
