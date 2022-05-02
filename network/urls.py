
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("Post/<str:post_id>", views.likes, name="likes"),
    path("follows/<str:user_id>", views.follows, name="follows"),
    path("following", views.following, name="following"),
    path("other_profile/<str:user_id>", views.other_profile, name="other_profile"),
    path("edit/<str:post_id>", views.edit, name="edit")
]
