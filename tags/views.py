from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
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
    
class UpdateTagView(LoginRequiredMixin, UpdateView):
    pass


