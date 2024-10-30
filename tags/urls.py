from django.urls import path
from .views import TagListView, NewTagView, UpdateTagView, DeleteTagView, BetTagPageView

urlpatterns = [
    path("", TagListView.as_view(), name="tag_list"),
    path("new_tag/", NewTagView.as_view(), name="new_tag"),
    path("update_tag/<int:pk>/", UpdateTagView.as_view(), name="update_tag"),
    path("delete_tag/<int:pk>/", DeleteTagView.as_view(), name="delete_tag"),
    path("bet_tag_page/<int:pk>/", BetTagPageView.as_view(), name="bet_tag_page"),


]
