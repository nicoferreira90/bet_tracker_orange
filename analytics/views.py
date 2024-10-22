from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView

class AnalyticsPageView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/analytics_page.html"
    login_url = "/users/login/"