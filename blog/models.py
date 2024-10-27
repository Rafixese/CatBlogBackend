from django.db import models

from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field
from typing import Any, List

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
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