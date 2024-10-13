# blog/urls.py
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter

# Create a router and register the PostViewSet
router = DefaultRouter()
router.register(r'api/posts', PostViewSet, basename='post')

# Define your URL patterns
urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),  # URL for signup
    path('home/', home, name='home'), 
    path('create-post/', create_post, name='create_post'),  # Create post URL
    path('post/<int:post_id>/', view_post, name='view_post'),  # View single post
    path('post/<int:post_id>/edit/', update_post, name='update_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('profile/', profile_view, name='profile_view'),
    path('profile/edit/', profile_edit, name='profile_edit'),  # Profile edit URL
    path('my-posts/', user_feed, name='user_feed'),
    
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    # Include the router URLs
] + router.urls
