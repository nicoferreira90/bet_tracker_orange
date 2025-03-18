from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomUserSettingsForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ["odds_preference", "items_per_page", "remove_color_from_tables"]
