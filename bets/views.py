from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.views.decorators.http import require_http_methods
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import BetForm, BetAmericanForm
from .models import Bet
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


class BetHistoryView(LoginRequiredMixin, ListView):
    model = Bet
    template_name = "bets/bet_history.html"
    login_url = reverse_lazy("account_login")

    def get_queryset(self):
        """Override the get_queryset method so that BetHistoryView only displays bets made by the current user."""
        return Bet.objects.filter(bet_owner=self.request.user).order_by("-date_added")

    def get_context_data(self, **kwargs):
        """Override the get_context_data method to pass the user's preferred odds format."""
        context = super().get_context_data(**kwargs)
        context["odds_preference"] = self.request.user.odds_preference
        context["table_color_preference_white"] = (
            self.request.user.remove_color_from_tables
        )
        return context

    def get_paginate_by(self, queryset):
        """Override the get_paginate_by method to set pagination based on the user's preference."""
        # Retrieve the user's preferred items per page (default to 20 if not set)
        items_per_page = self.request.user.items_per_page
        if items_per_page == "no":
            return None  # No pagination if 'no' is selected
        return int(
            items_per_page
        )  # Convert the string value to an integer for pagination


class NewBetView(LoginRequiredMixin, CreateView):
    model = Bet
    form_class = BetForm
    template_name = "bets/new_bet.html"
    success_url = reverse_lazy("bet_history")
    login_url = reverse_lazy("account_login")

    def get_form_class(self):
        # Select the appropriate form based on the user's odds preference
        if self.request.user.odds_preference == "decimal":
            return BetForm
        else:
            return BetAmericanForm

    def form_valid(self, form):
        # Set the owner of the bet to the current user

        print(f"Bet instance before saving: {form.instance.odds}")

        if not form.instance.odds:
            form.instance.odds = form.cleaned_data.get("odds")

        print(f"Bet instance before saving: {form.instance.odds}")

        form.instance.bet_owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["odds_preference"] = self.request.user.odds_preference
        return context


class UpdateBetView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Bet
    form_class = BetForm
    template_name = "bets/update_bet.html"
    success_url = reverse_lazy("bet_history")
    login_url = reverse_lazy("account_login")

    def get_form_class(self):
        # Select the appropriate form based on the user's odds preference
        if self.request.user.odds_preference == "decimal":
            return BetForm
        else:
            return BetAmericanForm

    def form_valid(self, form):
        # Set the owner of the bet to the current user

        print(f"Bet instance before saving: {form.instance.odds}")

        if not form.instance.odds:
            form.instance.odds = form.cleaned_data.get("odds")

        print(f"Bet instance before saving: {form.instance.odds}")

        form.instance.bet_owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """Checks if bet owner is the same as the current user."""
        obj = self.get_object()
        return obj.bet_owner == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["odds_preference"] = self.request.user.odds_preference
        return context

    def get_initial(self):
        initial = super().get_initial()
        bet = self.get_object()

        # Convert decimal odds to american odds if necessary
        if self.request.user.odds_preference == "american":
            initial["american_odds"] = Bet.decimal_to_american(bet.odds)

        return initial


@require_http_methods(["DELETE"])
@login_required
def delete_bet_view(request, pk):
    if request.user == Bet.objects.get(pk=pk).bet_owner:
        Bet.objects.get(pk=pk).delete()
        bet_list = Bet.objects.filter(bet_owner=request.user).order_by("-date_added")

        paginator = Paginator(bet_list, 20)
        page_obj = paginator.get_page(1)

        context = {
            "bet_list": bet_list,
            "page_obj": page_obj,
        }
        return render(request, "bets/partials/bet_history_table.html", context=context)
    else:
        raise PermissionDenied
