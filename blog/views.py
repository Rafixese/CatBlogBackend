from typing import cast
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status

from blog.models import Tag, Post, Comment
from blog.serializers import TagSerializer, CommentSerializer, PostSerializer
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework.permissions import BasePermission
from django.db.models.query import QuerySet
from rest_framework.serializers import BaseSerializer


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
    lookup_field = 'slug'

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
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
    def get_queryset(self) -> QuerySet:
        post_slug = self.kwargs.get('post_slug')
        if post_slug is not None:
            return Comment.objects.filter(post__slug=post_slug)
        else:
            return Comment.objects.none()

    def get_permissions(self) -> list[BasePermission]:
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return cast(list[BasePermission], super().get_permissions()) 
    
    def perform_create(self, serializer: BaseSerializer) -> None:
        post_slug = self.kwargs.get('post_slug')
        post = get_object_or_404(Post, slug=post_slug)
        serializer.save(post=post)
