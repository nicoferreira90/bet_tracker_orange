
from django.urls import path
from .views import HomePageView, AboutPageView, PasswordChangeSuccessView

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("about/", AboutPageView.as_view(), name="about_page"),
    path('accounts/password_change_success/', PasswordChangeSuccessView.as_view(), name="password_change_success")
]