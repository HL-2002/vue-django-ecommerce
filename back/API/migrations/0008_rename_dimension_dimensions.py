# Generated by Django 5.1.3 on 2024-11-12 18:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("API", "0007_alter_review_date"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Dimension",
            new_name="Dimensions",
        ),
    ]
