from django.shortcuts import render
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import BetForm
from .models import Bet


class BetHistoryView(ListView):
    model = Bet
    template_name = "bets/bet_history.html"

class NewBetView(CreateView):
    model = Bet
    form_class = BetForm
    template_name = "bets/new_bet.html"
    success_url = reverse_lazy("bet_history")

    def form_valid(self, form):
        # Set the owner of the bet to the current user
        form.instance.bet_owner = self.request.user
        return super().form_valid(form)

class DeleteBetView(DeleteView):
    model = Bet
    template_name = "bets/delete_bet.html"
    success_url = reverse_lazy("bet_history")

class UpdateBetView(UpdateView):
    model = Bet
    form_class = BetForm
    template_name = "bets/update_bet.html"
    success_url = reverse_lazy("bet_history")



