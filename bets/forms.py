from django import forms
from .models import Bet


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ["site", "bet_type", "pick", "stake", "odds", "result"]
