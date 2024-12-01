from django.db import models

from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from typing import Any, List
import textwrap

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField()
    content = CKEditor5Field()
    slug = models.SlugField(max_length=200, unique=True)
    published_date = models.DateTimeField(default=timezone.now)
    tags: models.ManyToManyField = models.ManyToManyField('Tag', related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})
    
class Comment(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    @property
    def truncated_content(self) -> str:
        return textwrap.shorten(self.content, width=100, placeholder="...")
        
    def __str__(self) -> str:
        return f'''{self.author} [{self.created_at}]: {self.truncated_content}'''
