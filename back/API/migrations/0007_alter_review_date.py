# Generated by Django 5.1.3 on 2024-11-12 17:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("API", "0006_category_unique_category_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="review",
            name="date",
            field=models.DateTimeField(),
        ),
    ]