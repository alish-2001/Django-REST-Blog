from rest_framework import serializers

from .models import Post,Comment,Category

class PostOutputSerializer(serializers.Serializer):

    id = serializers.IntegerField()
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



#Model Serializers
# class CommentSerializer(serializers.ModelSerializer):

#     commenter = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Comment
#         fields = ['commenter','title','text']
#         read_only_fields = ['user']

#     def get_commenter(self,comment):
#         return f"{comment.user.first_name} {comment.user.last_name}"

#     def create(self, validated_data):
#         post_id = self.context['post_pk']
#         user_id = self.context['user_id']
#         return Comment.objects.create(post_id=post_id, user_id=user_id, **validated_data)
        
# class PostSerializer(serializers.ModelSerializer):

#     likes_number = serializers.SerializerMethodField()

#     class Meta:
#         model = Post
#         fields = ['id','user','status','slug','likes_number','category','title','body','cover_image','created_at','edit_at',]
#         read_only_fields = ['id','user','status','slug','likes_number']
    
#     def get_likes_number(self,post):
#         return post.likes.count()

#     def create(self,validate_data):
#         user = self.context['user']
#         return Post.objects.create(user_id=user,**validate_data)
    
# class CategorySerializer(serializers.ModelSerializer):

#     category_posts_count = serializers.SerializerMethodField()

#     class Meta:
#         model = Category
#         fields = ['name','description','category_posts_count']

#     def get_category_posts_count(self,category):
#         return category.category_posts_count

# class CategoryDetailSerializer(serializers.ModelSerializer):

#     posts = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='post-detail')
    
#     class Meta:
#         model = Category
#         fields = ['name','posts']
