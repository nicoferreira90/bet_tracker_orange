import random
from django.core.management.base import BaseCommand
from faker import Faker
from bets.models import Bet
from users.models import CustomUser

from bets.models import BET_TYPE_CHOICES, RESULT_CHOICES


class Command(BaseCommand):
    help = 'Create fake bets'

    def handle(self, *args, **kwargs):
        fake = Faker()
        for _ in range(25):  # Adjust the range for the number of fake bets you want to create
            bet = Bet()
            bet.bet_owner = CustomUser.objects.get(pk=1)
            bet.site = fake.company()[:25]
            bet.pick = fake.text()[:25]
            bet.stake = round(random.uniform(1.0, 100.0), 2)
            bet.odds = round(random.uniform(1.0, 5.0), 3)
            bet.bet_type = fake.random_element(elements=[choice[0] for choice in BET_TYPE_CHOICES])
            bet.result = fake.random_element(elements=[choice[0] for choice in RESULT_CHOICES])
            bet.save()