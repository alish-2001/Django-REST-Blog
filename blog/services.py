from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

from blog.models import Like
from users.models import User
from .models import Post, Comment,Category

def post_create(*, data:dict, user:User):

    image = data.get('cover_image')
    if image:
        if image.size > 2 * 1024 * 1024:
            raise DRFValidationError("Image Size Must Be Less Than 3MB")
        
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
    
    try: 
        like = Like.objects.create(post=post, user=user)
    except (IntegrityError,DjangoValidationError):
        raise DRFValidationError("You Have Already Liked This Post")
    
    return like
