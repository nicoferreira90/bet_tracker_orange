# Generated by Django 5.1.1 on 2024-10-23 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0008_alter_bet_event_date_alter_bet_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='odds',
            field=models.DecimalField(decimal_places=3, max_digits=12),
        ),
    ]
