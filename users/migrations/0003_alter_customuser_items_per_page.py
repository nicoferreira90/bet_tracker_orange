# Generated by Django 5.1.1 on 2025-03-18 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_customuser_items_per_page_customuser_odds_preference_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="items_per_page",
            field=models.CharField(
                choices=[("decimal", "Decimal"), ("american", "American")],
                default="20",
                max_length=8,
            ),
        ),
    ]
