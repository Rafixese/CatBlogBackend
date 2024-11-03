from rest_framework import viewsets, permissions, status

from blog.models import Tag, Post, Comment
from blog.serializers import TagSerializer, CommentSerializer, PostSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve']:
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()
