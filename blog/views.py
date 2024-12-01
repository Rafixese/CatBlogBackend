from typing import cast
from rest_framework import viewsets, permissions, status

from blog.models import Tag, Post, Comment
from blog.serializers import TagSerializer, CommentSerializer, PostSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.permissions import BasePermission
from django.db.models.query import QuerySet

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    
    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        if search_query := self.request.query_params.get('search', None):
            search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
            search_query_obj = SearchQuery(search_query)
            queryset = queryset.annotate(
                rank=SearchRank(search_vector, search_query_obj)
            ).filter(rank__gte=0.1).order_by('-rank')
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self) -> list[BasePermission]:
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return cast(list[BasePermission], super().get_permissions()) 
