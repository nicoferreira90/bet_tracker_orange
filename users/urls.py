from django.urls import path
from .views import SignUpView, UserSettingsView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("user_settings/<int:pk>/", UserSettingsView.as_view(), name="user_settings"),
]
