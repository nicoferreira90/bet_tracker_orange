from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    ODDS_CHOICES = (
        ("decimal", "Decimal"),
        ("american", "American"),
    )

    PAGINATION_CHOICES = (
        ("10", 10),
        ("20", 20),
        ("50", 50),
        ("no", "No Pagination"),
    )

    odds_preference = models.CharField(
        max_length=8, choices=ODDS_CHOICES, default="decimal"
    )

    items_per_page = models.CharField(
        max_length=8, choices=PAGINATION_CHOICES, default="20"
    )

    remove_color_from_tables = models.BooleanField(default=False)
