from django import forms
from .models import Bet


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ["site", "bet_type", "pick", "stake", "odds", "result"]


class BetAmericanForm(forms.ModelForm):
    american_odds = forms.DecimalField(
        required=True, decimal_places=0, max_digits=10, label="American Odds"
    )

    class Meta:
        model = Bet
        fields = ["site", "pick", "stake", "bet_type", "result"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Reorder the fields
        self.fields = {
            "site": self.fields["site"],
            "bet_type": self.fields["bet_type"],
            "pick": self.fields["pick"],
            "stake": self.fields["stake"],
            "american_odds": self.fields["american_odds"],  # Place it second to last
            "result": self.fields["result"],  # Make sure result is last
        }

    def clean(self):
        cleaned_data = super().clean()
        american_odds = cleaned_data.get("american_odds")

        # Convert American odds to decimal
        if american_odds is not None:
            cleaned_data["odds"] = Bet.american_to_decimal(american_odds)
            print("this is working")

        print(f"Cleaned data: {cleaned_data}")

        return cleaned_data
