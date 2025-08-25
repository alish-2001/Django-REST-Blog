from .models import Post, Comment,Category
from users.models import User
from django.shortcuts import get_object_or_404

def post_create(*, data:dict, user:User):

    return Post.objects.create(**data, user=user)


def post_update(*, post:Post, data:dict, user:User):

    Post.objects.filter(pk=post.pk).update(user=user, **data)
    return Post.objects.get(pk=post.pk)


def comment_create(*, post:Post, data:dict, user:User):
    
    obj = Comment()
    obj.post = post
    obj.title = data.get('title', obj.title)
    obj.text = data.get('text', obj.text)
    obj.user = user
    obj.save()
    return obj


def category_create(*, data:dict, user:User):
    
    obj = Category()
    obj.name = data.get('name', obj.name)
    obj.description = data.get('description', obj.description)
    obj.user = user
    obj.save()
    return obj


def category_update(*, category:Category, data:dict):

    obj = category
    obj.name = data.get('name', obj.name)
    obj.description = data.get('description', obj.description)
    obj.save()
    return obj
