# Generated by Django 5.1.1 on 2024-11-25 21:31

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
            name='Bet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('site', models.CharField(blank=True, max_length=25, null=True)),
                ('pick', models.CharField(max_length=75)),
                ('stake', models.DecimalField(decimal_places=2, max_digits=12)),
                ('odds', models.DecimalField(decimal_places=3, max_digits=12)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('bet_type', models.CharField(choices=[('Spread', 'Spread'), ('Moneyline', 'Moneyline'), ('Futures', 'Futures'), ('Teaser', 'Teaser'), ('Total', 'Total'), ('Props', 'Props')], max_length=25)),
                ('result', models.CharField(choices=[('Win', 'Win'), ('Lose', 'Lose'), ('Push', 'Push'), ('Pending', 'Pending')], max_length=25)),
                ('bet_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
