from django.urls import path
from .views import BetHistoryView, NewBetView, UpdateBetView, delete_bet_view

urlpatterns = [
    path("history/", BetHistoryView.as_view(), name="bet_history"),
    path("new_bet/", NewBetView.as_view(), name="new_bet"),
    path("update_bet/<uuid:pk>/", UpdateBetView.as_view(), name="update_bet"),
    path("", BetHistoryView.as_view(), name="bet_history"),
]

htmx_urlpatterns = [
    path("delete_bet/<uuid:pk>/", delete_bet_view, name="delete_bet"),
]

urlpatterns += urlpatterns + htmx_urlpatterns
