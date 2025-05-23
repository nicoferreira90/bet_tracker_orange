import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from .analytics import bet_payout

RESULT_CHOICES = [
    ("Win", "Win"),
    ("Lose", "Lose"),
    ("Push", "Push"),
    ("Pending", "Pending"),
]

BET_TYPE_CHOICES = [
    ("Spread", "Spread"),
    ("Moneyline", "Moneyline"),
    ("Futures", "Futures"),
    ("Teaser", "Teaser"),
    ("Total", "Total"),
    ("Props", "Props"),
    ("Parlay", "Parlay"),
]


class Bet(models.Model):
    """Model a single bet in the database. These are standard bets, not parlays."""

    """class Meta:
            ordering = ['-date_added'] """  # for now keep bets in older to newer order

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # new
    bet_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    site = models.CharField(max_length=25, blank=True, null=True)
    pick = models.CharField(max_length=75)
    stake = models.DecimalField(max_digits=12, decimal_places=2)
    odds = models.DecimalField(max_digits=12, decimal_places=3)
    date_added = models.DateTimeField(auto_now_add=True)
    bet_type = models.CharField(max_length=25, choices=BET_TYPE_CHOICES)
    result = models.CharField(max_length=25, choices=RESULT_CHOICES)

    @staticmethod
    def american_to_decimal(american_odds):
        if american_odds > 0:
            return (american_odds / 100) + 1
        else:
            return (100 / abs(american_odds)) + 1

    @staticmethod
    def decimal_to_american(decimal_odds):
        if decimal_odds > 2:
            return round((decimal_odds - 1) * 100)  # Round the result to a whole number
        else:
            return round(
                -100 / (decimal_odds - 1)
            )  # Round the result to a whole number

    # In Django (and Python more generally), the @property decorator is a built-in feature that allows you to define methods in a class that can be accessed like attributes.
    @property
    def payout(self):
        if self.result == "Pending":
            return bet_payout(self.stake, self.odds, self.result)
        else:
            payout_value = bet_payout(self.stake, self.odds, self.result)
            return round(float(payout_value), 2)

    def __str__(self):
        return self.pick[:30]

    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})
