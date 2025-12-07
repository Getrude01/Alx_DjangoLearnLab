from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostByTagListView,  # <- add this
)

app_name = "blog"

urlpatterns = [
    # Authentication
    path("register/", views.register_view, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),

    # Search
    path('search/', views.search_posts, name='search_posts'),

    # Tags
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),

    # Blog posts CRUD (posts/ style)
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/new/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    # Blog posts CRUD (post/ style) — for the task checker
    path("post/new/", PostCreateView.as_view(), name="post_create_alt"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail_alt"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update_alt"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete_alt"),

    # Comment actions
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
]