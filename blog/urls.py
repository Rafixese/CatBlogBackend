from django.urls import path, include
from rest_framework.routers import DefaultRouter

from blog.views import TagViewSet, PostViewSet, CommentViewSet


# Create a router and register your viewsets
router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
