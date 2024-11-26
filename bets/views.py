from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import BetForm
from .models import Bet


class BetHistoryView(LoginRequiredMixin, ListView):
    model = Bet
    template_name = "bets/bet_history.html"
    login_url = reverse_lazy("account_login")
    paginate_by = 20

    def get_queryset(self):
        """Override the get_queryset method so that BetHistoryView only displays bets made by the current user."""
        return Bet.objects.filter(bet_owner=self.request.user).order_by('-date_added')

class NewBetView(LoginRequiredMixin, CreateView):
    model = Bet
    form_class = BetForm
    template_name = "bets/new_bet.html"
    success_url = reverse_lazy("bet_history")
    login_url = reverse_lazy("account_login")

    def form_valid(self, form):
        # Set the owner of the bet to the current user
        form.instance.bet_owner = self.request.user
        return super().form_valid(form)

class DeleteBetView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Bet
    template_name = "bets/delete_bet.html"
    success_url = reverse_lazy("bet_history")
    login_url = reverse_lazy("account_login")

    def test_func(self):
        """Checks if bet owner is the same as the current user."""
        obj = self.get_object()
        return obj.bet_owner == self.request.user

class UpdateBetView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bet
    form_class = BetForm
    template_name = "bets/update_bet.html"
    success_url = reverse_lazy("bet_history")
    login_url = reverse_lazy("account_login")

    def test_func(self):
        """Checks if bet owner is the same as the current user."""
        obj = self.get_object()
        return obj.bet_owner == self.request.user



