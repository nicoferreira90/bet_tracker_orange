from django.urls import path
from .views import AnalyticsPageView

urlpatterns = [
    path("", AnalyticsPageView.as_view(), name="analytics_page"),
]
