from django.contrib import admin
from .models import Like, Post,Comment,Category
# Register your models here.

@admin.register(Post)
class BlogPostAdmin(admin.ModelAdmin):
    list_display=['id', 'title','body',]


@admin.register(Category)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display=['id', 'name','description']


@admin.register(Comment)
class BlogPostCommentAdmin(admin.ModelAdmin):
    list_display=['id', 'title', 'text','user']


@admin.register(Like)
class BlogPostLike(admin.ModelAdmin):
    list_display=['id', 'post', 'user','liked_at']
