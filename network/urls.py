
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="new_post"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow", views.follow, name= "follow"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("following_page", views.following_page, name="following_page"),
    path("edit/<int:id>", views.edit, name="edit"),
    path("like/<int:post_id>", views.like, name="like"),
    path("unlike/<int:post_id>", views.unlike, name="unlike"),
]
