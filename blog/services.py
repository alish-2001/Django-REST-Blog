from blog.models import Like

from users.models import User
from .models import Post, Comment,Category

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
    

    return Comment.objects.create(post=post, user=user, **data)

def like_create(*, post:Post, user:User):
    
    like = Like.objects.create(post=post, user=user)
    return like
