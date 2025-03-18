from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


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
    ]


admin.site.register(CustomUser, CustomUserAdmin)
