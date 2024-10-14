from django.db import models
from django.conf import settings
from django.urls import reverse
from .analytics import bet_payout

RESULT_CHOICES = [

        ('Win', "Win"),
        ('Lose', 'Lose'),
        ('Push', 'Push'),
        ('Pending', 'Pending'),
    
]

class Bet(models.Model):
    """Model a single bet in the database. These are standard bets, not parlays."""

    class Meta:
       ordering = ['-date_added']

    bet_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    site = models.CharField(max_length=25, blank=True, null=True)
    pick = models.CharField(max_length=50)
    stake = models.DecimalField(max_digits=12, decimal_places=2)
    odds = models.DecimalField(max_digits=12, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    event_date = models.DateField(blank=True, null=True)
    result = models.CharField(max_length=25, choices=RESULT_CHOICES)


    # In Django (and Python more generally), the @property decorator is a built-in feature that allows you to define methods in a class that can be accessed like attributes.
    @property
    def payout(self):
        if self.result == "Pending":
            return bet_payout(self.stake, self.odds, self.result)
        else:
            payout_value = bet_payout(self.stake, self.odds, self.result)
            return round(float(payout_value), 2)

    def __str__(self):
        return self.pick
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})
