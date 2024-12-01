# tests.py

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Tag, Post, Comment


class BlogAPITestCase(APITestCase):
    def setUp(self) -> None:
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='password'
        )

        # Initialize the APIClient
        self.client = APIClient()

        # Create test data
        self.tag = Tag.objects.create(name='TestTag')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            slug='test-post',
        )
        self.post.tags.add(self.tag)
        self.comment = Comment.objects.create(
            author='Guest',
            content='Test Comment',
            post=self.post,
        )

        # Endpoints
        self.tag_list_url = reverse('tag-list')
        self.tag_detail_url = reverse('tag-detail', kwargs={'pk': self.tag.pk})

        self.post_list_url = reverse('post-list')
        self.post_detail_url = reverse('post-detail', kwargs={'pk': self.post.pk})

        self.comment_list_url = reverse('comment-list')
        self.comment_detail_url = reverse('comment-detail', kwargs={'pk': self.comment.pk})

    # TagViewSet Tests
    def test_tag_list_guest(self) -> None:
        response = self.client.get(self.tag_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_retrieve_guest(self) -> None:
        response = self.client.get(self.tag_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_create_guest(self) -> None:
        data = {'name': 'NewTag'}
        response = self.client.post(self.tag_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_update_guest(self) -> None:
        data = {'name': 'UpdatedTag'}
        response = self.client.put(self.tag_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_delete_guest(self) -> None:
        response = self.client.delete(self.tag_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_create_admin(self) -> None:
        self.client.login(username='admin', password='password')
        data = {'name': 'AdminTag'}
        response = self.client.post(self.tag_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_tag_update_admin(self) -> None:
        self.client.login(username='admin', password='password')
        data = {'name': 'AdminUpdatedTag'}
        response = self.client.put(self.tag_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_delete_admin(self) -> None:
        self.client.login(username='admin', password='password')
        response = self.client.delete(self.tag_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # PostViewSet Tests
    def test_post_list_guest(self) -> None:
        response = self.client.get(self.post_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_retrieve_guest(self) -> None:
        response = self.client.get(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_create_guest(self) -> None:
        data = {'title': 'Guest Post', 'content': 'Content', 'slug': 'guest-post'}
        response = self.client.post(self.post_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_update_guest(self) -> None:
        data = {'title': 'Updated Guest Post', 'content': 'Updated Content', 'slug': 'test-post'}
        response = self.client.put(self.post_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_guest(self) -> None:
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_create_admin(self) -> None:
        self.client.login(username='admin', password='password')
        data = {
            'title': 'Admin Post',
            'content': 'Admin Content',
            'slug': 'admin-post',
        }
        response = self.client.post(self.post_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_update_admin(self) -> None:
        self.client.login(username='admin', password='password')
        data = {
            'title': 'Updated Admin Post',
            'content': 'Updated Admin Content',
            'slug': 'test-post',
        }
        response = self.client.put(self.post_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete_admin(self) -> None:
        self.client.login(username='admin', password='password')
        response = self.client.delete(self.post_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # CommentViewSet Tests
    def test_comment_list_guest(self) -> None:
        response = self.client.get(self.comment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_retrieve_guest(self) -> None:
        response = self.client.get(self.comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_create_guest(self) -> None:
        data = {
            'author': 'GuestUser',
            'content': 'New Comment Content',
            'post': self.post.id,
        }
        response = self.client.post(self.comment_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_update_guest(self) -> None:
        data = {
            'author': 'GuestUser',
            'content': 'Updated Comment Content',
            'post': self.post.id,
        }
        response = self.client.put(self.comment_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_delete_guest(self) -> None:
        response = self.client.delete(self.comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_update_admin(self) -> None:
        self.client.login(username='admin', password='password')
        data = {
            'author': 'AdminUser',
            'content': 'Admin Updated Comment',
            'post': self.post.id,
        }
        response = self.client.put(self.comment_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_delete_admin(self) -> None:
        self.client.login(username='admin', password='password')
        response = self.client.delete(self.comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
