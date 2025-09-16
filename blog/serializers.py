from rest_framework import serializers
from .models import Category

class PostOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField()
    status = serializers.CharField(max_length=5)
    likes_number = serializers.IntegerField(default=0)
    comments_numbr = serializers.IntegerField(default=0)
    title = serializers.CharField(max_length=200)
    category = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=2000)
    cover_image = serializers.ImageField(use_url=True)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

class PostInputSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    title = serializers.CharField(max_length=100)
    body = serializers.CharField(max_length=2000)   
    cover_image = serializers.ImageField(allow_null=True, required=False,)

class CommentOutputSerializer(serializers.Serializer):
    post = serializers.HyperlinkedRelatedField(view_name='post-detail', read_only=True)
    user = serializers.StringRelatedField()
    title = serializers.CharField(max_length=200)
    text = serializers.CharField(max_length=2000)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField() 

class CommentInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    text = serializers.CharField(max_length=2000)

class CategoryOutputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    post = serializers.HyperlinkedRelatedField(view_name='post-detail', read_only=True)
    posts_number = serializers.IntegerField(default=0)

class CategoryInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=500,)
