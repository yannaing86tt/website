from django.urls import path
from . import views
from . import views_posts
from . import views_public
from . import views_media
from . import views_md
from . import views_auth

urlpatterns = [
    # Authentication (public)
    path("register/", views_auth.register_view, name="register"),
    path("login/", views_auth.login_view, name="login"),
    path("logout/", views_auth.logout_view, name="logout"),
    
    # Media (panel)
    path("panel/media/", views_media.panel_media_list, name="panel_media_list"),
    path("panel/media/new/", views_media.panel_media_new, name="panel_media_new"),
    path("panel/media/<int:pk>/edit/", views_media.panel_media_edit, name="panel_media_edit"),
    path("panel/media/<int:pk>/delete/", views_media.panel_media_delete, name="panel_media_delete"),

    path("panel/media/<int:pk>/tracks/", views_media.panel_media_tracks, name="panel_media_tracks"),
    path("panel/media/track/<int:pk>/delete/", views_media.panel_media_track_delete, name="panel_media_track_delete"),


    # Media (public)
    path("library/", views_media.media_list, name="media_list"),
    path("library/<str:kind>/", views_media.media_list, name="media_list_kind"),
    path("library/item/<slug:slug>/", views_media.media_detail, name="media_detail"),
    
    # public
    path("", views.home, name="home"),
    path("posts/", views_public.posts_list, name="posts_list_public"),
    path("posts/<str:slug>/", views_public.post_detail, name="post_detail"),

    # panel
    path("panel/", views.panel_dashboard, name="panel_dashboard"),
    path("panel/login/", views.panel_login, name="panel_login"),
    path("panel/logout/", views.panel_logout, name="panel_logout"),

    path("panel/md-preview/", views_md.md_preview, name="md_preview"),

    # User management (superadmin only)
    path("panel/users/", views.user_list, name="user_list"),
    path("panel/users/new/", views.user_create, name="user_create"),
    path("panel/users/<int:user_id>/edit/", views.user_edit, name="user_edit"),
    path("panel/users/<int:user_id>/delete/", views.user_delete, name="user_delete"),

    # Posts
    path("panel/posts/", views_posts.post_list, name="post_list"),
    path("panel/posts/new/", views_posts.post_create, name="post_create"),
    path("panel/posts/<int:post_id>/edit/", views_posts.post_edit, name="post_edit"),
    path("panel/posts/<int:post_id>/delete/", views_posts.post_delete, name="post_delete"),
]
