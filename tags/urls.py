from django.urls import path
from .views import TagListView, NewTagView, UpdateTagView

urlpatterns = [
    path("", TagListView.as_view(), name="tag_list"),
    path("new_tag/", NewTagView.as_view(), name="new_tag"),
    path("update_tag/", UpdateTagView.as_view(), name="update_tag")


]
