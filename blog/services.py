from .models import Post, Comment,Category
from users.models import User

def post_create(*, data:dict, user:User):

    obj = Post()
    obj.category = data.get('category', obj.category)
    obj.title = data.get('title', obj.title)
    obj.body = data.get('body', obj.body)
    obj.cover_image = data.get('cover_image', obj.cover_image)
    obj.user = user
    obj.save()
    return obj


def post_update(*, post:Post, data:dict, user:User):

    obj = post
    obj.category = data.get('category', obj.category)
    obj.title = data.get('title', obj.title)
    obj.body = data.get('body', obj.body)
    obj.cover_image = data.get('cover_image', obj.cover_image)
    obj.user = user
    obj.save()
    return obj


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
