from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import login_view

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('login', login_view, name='login'),
]