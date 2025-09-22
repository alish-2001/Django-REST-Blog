from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound as DRFNotFound

from .models import Post,Category,Comment

def get_post_queryset():
    return Post.objects.filter(status='pub').select_related('category','user').annotate(likes_number=Count('likes'),comments_numbr=Count('comments')).order_by('-created_at')

def get_post_object(pk:int):
    try:
        return Post.objects.select_related('category','user').annotate(likes_number=Count('likes'),comments_numbr=Count('comments')).get(pk=pk)
    except Post.DoesNotExist:
        raise DRFNotFound("Post Not Found")
    
def get_category_queryset():
    return Category.objects.annotate(posts_number=Count('posts')).all()

def get_category_object(pk:int):
    try:
        return Category.objects.annotate(posts_number=Count('posts')).get(pk=pk)
    except Category.DoesNotExist:
        raise DRFNotFound("Category Not Found")
    

def get_comment_queryset(pk:int):
   return Comment.objects.filter(post=pk, status='a').select_related('post', 'user')

def get_comment_object(post_pk:int, comment_pk:int):
    try:
        return Comment.objects.get(post=post_pk, pk=comment_pk)
    except Comment.DoesNotExist:
        raise DRFNotFound("Comment Not Found")
   

