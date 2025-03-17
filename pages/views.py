from django.shortcuts import render, redirect
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home_page.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Redirect or render a different template if logged in
            return redirect("bets/history/")
        return super().dispatch(request, *args, **kwargs)


class AboutPageView(TemplateView):
    template_name = "about_page.html"


class PasswordChangeSuccessView(TemplateView):
    template_name = "account/password_change_done.html"

class VersionHistoryPageView(TemplateView):
    template_name = "version_history.html"