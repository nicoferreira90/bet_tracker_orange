from django.urls import path
from .views import TagListView, NewTagView, UpdateTagView, DeleteTagView, BetTagPageView, BetNewTagView, remove_associated_tag, add_associated_tag

urlpatterns = [
    path("", TagListView.as_view(), name="tag_list"),
    path("new_tag/", NewTagView.as_view(), name="new_tag"),
    path("update_tag/<uuid:pk>/", UpdateTagView.as_view(), name="update_tag"),
    path("delete_tag/<uuid:pk>/", DeleteTagView.as_view(), name="delete_tag"),
    path("bet_tag_page/<uuid:pk>/", BetTagPageView.as_view(), name="bet_tag_page"),
    path("bet_new_tag/", BetNewTagView.as_view(), name="bet_new_tag"),

]

htmx_urlpatterns = [
    path("remove_associated_tag/<uuid:pk>/", remove_associated_tag, name="remove_associated_tag"),
    path("add_associated_tag/<uuid:pk>/", add_associated_tag, name="add_associated_tag"),
]

urlpatterns = urlpatterns + htmx_urlpatterns