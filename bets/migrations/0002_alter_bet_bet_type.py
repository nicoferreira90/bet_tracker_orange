# Generated by Django 5.1.1 on 2024-12-19 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bet',
            name='bet_type',
            field=models.CharField(choices=[('Spread', 'Spread'), ('Moneyline', 'Moneyline'), ('Futures', 'Futures'), ('Teaser', 'Teaser'), ('Total', 'Total'), ('Props', 'Props'), ('Parlay', 'Parlay')], max_length=25),
        ),
    ]
