
from django.urls import path
from .views import BetHistoryView, NewBetView, DeleteBetView, UpdateBetView

urlpatterns = [
    path("history/", BetHistoryView.as_view(), name="bet_history"),
    path("new_bet/", NewBetView.as_view(), name="new_bet"),
    path("delete_bet/<uuid:pk>/", DeleteBetView.as_view(), name="delete_bet"),
    path("update_bet/<uuid:pk>/", UpdateBetView.as_view(), name="update_bet"),
    path("", BetHistoryView.as_view(), name="bet_history"),

]
