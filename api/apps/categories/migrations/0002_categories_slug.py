# Generated by Django 5.1.4 on 2024-12-08 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="categories",
            name="slug",
            field=models.SlugField(default="default-slug", unique=True),
            preserve_default=False,
        ),
    ]
