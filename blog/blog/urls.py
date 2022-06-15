from django.contrib import admin
from django.urls import include, path

from app.views import (
    PostAPIViews,
    PostSubscribeDetailViews,
    PostSubscribeListViews,
    SubscribeView,
    UserListViews,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/post/", PostAPIViews.as_view(), name="post"),
    path("api/subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("api/authors/", UserListViews.as_view(), name="authors"),
    path("api/post_subscribe/", PostSubscribeListViews.as_view(), name="post_subscribe"),
    path("api/post_subscribe/<int:pk>/", PostSubscribeDetailViews.as_view(), name="post_subscribe_detail"),
]
