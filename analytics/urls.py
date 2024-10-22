
from django.urls import path
from .views import AnalyticsPageView, AnalyticsWithResultsView

urlpatterns = [
    path("", AnalyticsPageView.as_view(), name="analytics_page"),
    path("results/", AnalyticsWithResultsView.as_view(), name="analytics_results"),

]
