from django import forms
from .models import Bet

class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['site', 'pick', 'stake', 'odds', 'event_date', 'result']