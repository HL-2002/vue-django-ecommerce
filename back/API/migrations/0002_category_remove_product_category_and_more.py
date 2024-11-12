# Generated by Django 5.1.3 on 2024-11-12 14:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("API", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name="product",
            name="category",
        ),
        migrations.RemoveField(
            model_name="tag",
            name="product_id",
        ),
        migrations.AddField(
            model_name="product",
            name="category_id",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="API.category",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="productTag",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("tag_id", models.CharField(max_length=100)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="API.product"
                    ),
                ),
            ],
        ),
    ]