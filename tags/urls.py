from django.urls import path
from .views import TagListView, NewTagView, UpdateTagView, DeleteTagView, BetTagPageView, BetNewTagView

urlpatterns = [
    path("", TagListView.as_view(), name="tag_list"),
    path("new_tag/", NewTagView.as_view(), name="new_tag"),
    path("update_tag/<uuid:pk>/", UpdateTagView.as_view(), name="update_tag"),
    path("delete_tag/<uuid:pk>/", DeleteTagView.as_view(), name="delete_tag"),
    path("bet_tag_page/<uuid:pk>/", BetTagPageView.as_view(), name="bet_tag_page"),
    path("bet_new_tag/", BetNewTagView.as_view(), name="bet_new_tag"),

]
