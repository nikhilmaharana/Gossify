# apps/posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Feed & Post CRUD
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
    path('my-posts/', views.user_posts, name='user_posts'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    # ⭐ New Like & Comment routes
    path('posts/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
]
