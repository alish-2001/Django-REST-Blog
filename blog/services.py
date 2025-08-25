from .models import Post, Comment,Category
from users.models import User
from django.shortcuts import get_object_or_404

def post_create(*, data:dict, user:User):

    return Post.objects.create(**data, user=user)


def post_update(*, post:Post, data:dict, user:User):

    Post.objects.filter(pk=post.pk).update(user=user, **data)
    return Post.objects.get(pk=post.pk)


def category_create(*, data:dict):
    
    return Category.objects.create(**data)


def category_update(*, category:Category, data:dict):

    Category.objects.filter(pk=category.pk).update(**data)
    return Category.objects.get(pk=category.pk)

def comment_create(*, post:Post, data:dict, user:User):
    
    obj = Comment()
    obj.post = post
    obj.title = data.get('title', obj.title)
    obj.text = data.get('text', obj.text)
    obj.user = user
    obj.save()
    return obj
