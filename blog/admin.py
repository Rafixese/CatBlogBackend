from django.contrib import admin

from blog.models import Post, Tag, Comment

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'slug')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('published_date', 'tags')
    date_hierarchy = 'published_date'
    filter_horizontal = ('tags',)
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'truncated_content')
    search_fields = ('author', 'truncated_content')
    list_filter = ('post__title', 'author', 'created_at')
    date_hierarchy = 'created_at'
