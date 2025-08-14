from rest_framework import serializers

from .models import Post,Comment,Category

class CommentSerializer(serializers.ModelSerializer):

    commenter = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['commenter','title','text']
        read_only_fields = ['user']

    def get_commenter(self,comment):
        return f"{comment.user.first_name} {comment.user.last_name}"

    def create(self, validated_data):
        post_id = self.context['post_pk']
        user_id = self.context['user_id']
        return Comment.objects.create(post_id=post_id, user_id=user_id, **validated_data)
        
class PostSerializer(serializers.ModelSerializer):

    likes_number = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','user','status','slug','likes_number','category','title','body','cover_image','created_at','edit_at',]
        read_only_fields = ['id','user','status','slug','likes_number']
    
    def get_likes_number(self,post):
        return post.likes.count()

    def create(self,validate_data):
        user = self.context['user']
        return Post.objects.create(user_id=user,**validate_data)
    
class CategorySerializer(serializers.ModelSerializer):

    category_posts_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['name','description','category_posts_count']

    def get_category_posts_count(self,category):
        return category.category_posts_count

class CategoryDetailSerializer(serializers.ModelSerializer):

    posts = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='post-detail')
    
    class Meta:
        model = Category
        fields = ['name','posts']