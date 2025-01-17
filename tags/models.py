import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from bets.models import Bet
from users.models import CustomUser


class Tag(models.Model):
    """Model a single Tag, which is a label associated with one or more bets."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # new
    associated_bets = models.ManyToManyField(Bet, related_name="tags", blank=True)
    label = models.CharField(max_length=25)
    description = models.CharField(max_length=50, blank=True)
    tag_owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.label
