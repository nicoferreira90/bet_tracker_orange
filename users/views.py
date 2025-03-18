from .forms import CustomUserCreationForm, CustomUserSettingsForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class UserSettingsView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    login_url = reverse_lazy("account_login")
    template_name = "account/settings.html"
    form_class = CustomUserSettingsForm
    success_url = reverse_lazy("home_page")
