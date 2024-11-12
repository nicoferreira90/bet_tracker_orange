
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('kbzon/', admin.site.urls),
    path('users/', include("users.urls") ),
    path('users/', include("django.contrib.auth.urls")),
    path('bets/', include("bets.urls")),
    path('', include("pages.urls")),
    path('analytics/', include("analytics.urls")),
    path('tags/', include("tags.urls")),
] + debug_toolbar_urls()
