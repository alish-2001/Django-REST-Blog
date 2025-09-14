from django.db.models import Count
from django.shortcuts import get_object_or_404

from .models import Post,Category,Comment

def get_post_queryset():
    return Post.objects.filter(status='pub').select_related('category','user').annotate(likes_number=Count('likes'),comments_numbr=Count('comments')).order_by('-created_at')

def get_post_object(pk:int):
    return get_object_or_404(Post.objects.select_related('category','user').annotate(likes_number=Count('likes'),comments_numbr=Count('comments')),pk=pk)

def get_category_queryset():
    return Category.objects.annotate(posts_number=Count('posts')).all()

def get_category_object(pk:int):
    return get_object_or_404(Category.objects.annotate(posts_number=Count('posts')), pk=pk)

def get_comment_queryset(pk:int):
   return Comment.objects.filter(post=pk, status='a').select_related('post', 'user')

def get_comment_object(post_pk:int, comment_pk:int):
   return get_object_or_404(Comment, post=post_pk, pk=comment_pk)

