
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("users.urls") ),
    path('users/', include("django.contrib.auth.urls")),
    path('bets/', include("bets.urls")),
    path('', include("pages.urls")),
    path('analytics/', include("analytics.urls")),
    path('tags/', include("tags.urls")),
]
