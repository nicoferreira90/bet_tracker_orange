from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from bets.models import Bet


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "pk",
        "email",
        "username",
        "is_staff",
        "odds_preference",
        "items_per_page",
        "remove_color_from_tables",
        "get_bet_count",
    ]

    def get_bet_count(self, obj):
        return Bet.objects.filter(
            bet_owner=obj
        ).count()  # Count the number of Bet objects related to this user

    get_bet_count.short_description = "Number of Bets"  # Set a custom column name


admin.site.register(CustomUser, CustomUserAdmin)
