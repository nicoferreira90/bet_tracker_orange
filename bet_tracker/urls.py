from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from allauth.account import views as allauth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

urlpatterns = [
    path("kbzon/", admin.site.urls),
    path(
        "accounts/password/change/",
        login_required(
            allauth_views.PasswordChangeView.as_view(
                success_url=reverse_lazy("password_change_success")
            )
        ),
        name="account_change_password",
    ),
    path("accounts/", include("allauth.urls")),
    path("bets/", include("bets.urls")),
    path("", include("pages.urls")),
    path("analytics/", include("analytics.urls")),
    path("tags/", include("tags.urls")),
] + debug_toolbar_urls()
