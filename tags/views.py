from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import Tag
from .forms import TagForm
from bets.models import Bet

class TagListView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "tags/tag_list.html"
    login_url = "/users/login/"

class NewTagView(LoginRequiredMixin, CreateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/new_tag.html"
    login_url = "/users/login/"
    success_url = reverse_lazy("tag_list")

    def form_valid(self, form):
        # Set the owner of the bet to the current user
        form.instance.tag_owner = self.request.user
        return super().form_valid(form)
    
class UpdateTagView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tag
    form_class = TagForm
    template_name = "tags/update_tag.html"
    login_url = "/users/login/"
    success_url = reverse_lazy("tag_list")

    def test_func(self):
        """Checks if bet owner is the same as the current user."""
        obj = self.get_object()
        return obj.tag_owner == self.request.user

class DeleteTagView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tag
    template_name = "tags/delete_tag.html"
    success_url = reverse_lazy("tag_list")
    login_url = login_url = "/users/login/"

    def test_func(self):
        """Checks if bet owner is the same as the current user."""
        obj = self.get_object()
        return obj.tag_owner == self.request.user
    
class BetTagPageView(LoginRequiredMixin, UserPassesTestMixin, DetailView):

    model = Bet
    template_name = "tags/bet_tag_page.html"

    def test_func(self):
        """Checks if bet owner is the same as the current user."""
        obj = self.get_object()
        return obj.bet_owner == self.request.user