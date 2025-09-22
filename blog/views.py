from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import serializers

from .models import Category
from .permissions import IsPostAuthor
from .services import category_create, category_update, like_create, post_create,comment_create,post_update
from .selectors import get_comment_object, get_post_queryset,get_post_object,get_comment_queryset,get_category_queryset,get_category_object
from .schemas import post_list_schema,post_create_schema,post_detail_schema,post_update_schema,post_delete_schema,comment_list_schema,comment_create_schema,comment_delete_schema,like_create_schema,category_list_schema,category_detail_schema,category_create_schema,category_update_schema,category_delete_schema

class PostListView(APIView):

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

    @post_list_schema
    def get(self, request):
        posts = get_post_queryset() 
        serializer = self.PostOutputSerializer(posts, context={'request':request}, many=True)
        return Response(serializer.data)

class PostCreateView(APIView):

    class PostInputSerializer(serializers.Serializer):
        category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
        title = serializers.CharField(max_length=100)
        body = serializers.CharField(max_length=2000)   
        cover_image = serializers.ImageField(allow_null=True, required=False,)

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


    permission_classes = [IsAuthenticated]

    @post_create_schema
    def post(self, request):
        serializer = self.PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = post_create(data=serializer.validated_data, user=request.user)
        output = self.PostOutputSerializer(post, context={"request": request})
        return Response(output.data, status=status.HTTP_201_CREATED)

class PostDetailView(APIView):

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

    @post_detail_schema
    def get(self, request, pk):
        post = get_post_object(pk=pk)
        serializer = self.PostOutputSerializer(post, context={'request':request})
        return Response(serializer.data)

class PostUpdateView(APIView):

    class PostInputSerializer(serializers.Serializer):
        category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
        title = serializers.CharField(max_length=100)
        body = serializers.CharField(max_length=2000)   
        cover_image = serializers.ImageField(allow_null=True, required=False,)

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

    permission_classes = [IsPostAuthor]

    @post_update_schema
    def put(self, request, pk):

        post = get_post_object(pk=pk)
        self.check_object_permissions(request, post)
        serializer = self.PostInputSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        post = post_update(post=post, data=serializer.validated_data, user=request.user)
        output = self.PostOutputSerializer(post, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)
    
    @post_update_schema
    def patch(self, request, pk):
        post = get_post_object(pk=pk)
        self.check_object_permissions(request=request, obj=post)
        serializer = PostInputSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        post = post_update(post=post, data=serializer.validated_data, user=request.user)
        output = PostOutputSerializer(post, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

class PostDeleteView(APIView):

    permission_classes = [IsPostAuthor]
    
    @post_delete_schema
    def delete(self, request, pk):
        post = get_post_object(pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

class CommentListView(APIView):

    class CommentOutputSerializer(serializers.Serializer):
        post = serializers.HyperlinkedRelatedField(view_name='post-detail', read_only=True)
        user = serializers.StringRelatedField()
        title = serializers.CharField(max_length=200)
        text = serializers.CharField(max_length=2000)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField() 


    @comment_list_schema
    def get(self, request, pk):

        comments = get_comment_queryset(pk=pk) 
        serializer = self.CommentOutputSerializer(comments, context={'request':request}, many=True)
        return Response(serializer.data)

class CommentCreateView(APIView):

    class CommentInputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=200)
        text = serializers.CharField(max_length=2000)

    class CommentOutputSerializer(serializers.Serializer):
        post = serializers.HyperlinkedRelatedField(view_name='post-detail', read_only=True)
        user = serializers.StringRelatedField()
        title = serializers.CharField(max_length=200)
        text = serializers.CharField(max_length=2000)
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField() 

    permission_classes = [IsAuthenticated]

    @comment_create_schema
    def post(self, request, pk):
        
        post = get_post_object(pk=pk)
        serializer = self.CommentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = comment_create(post=post, data=serializer.validated_data, user=request.user) 
        return Response(self.CommentOutputSerializer(comment, context={'request':request}).data, status=status.HTTP_201_CREATED)

class CommentDeleteView(APIView):

    permission_classes = [IsAdminUser]

    @comment_delete_schema
    def delete(self, request, post_pk, comment_pk):
        comment = get_comment_object(post_pk=post_pk, comment_pk=comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  

class LikeCreateView(APIView):
   
    permission_classes = [IsAuthenticated]

    @like_create_schema
    def post(self, request, pk):

        post = get_post_object(pk=pk)
        user = request.user
        like_create(post=post, user=user)
        return Response(status=status.HTTP_201_CREATED)

class CategoryListView(APIView):

    class CategoryOutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField(max_length=200)
        post = serializers.HyperlinkedRelatedField(view_name='post-detail', read_only=True)
        posts_number = serializers.IntegerField(default=0)

    @category_list_schema
    def get(self,request):
        categories = get_category_queryset() 
        serializer = self.CategoryOutputSerializer(categories, context={'request':request}, many=True)
        return Response(serializer.data)

class CategoryDetailView(APIView):

    class CategoryOutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        name = serializers.CharField(max_length=200)
        post = serializers.HyperlinkedRelatedField(view_name='post-detail', read_only=True)
        posts_number = serializers.IntegerField(default=0)

    @category_detail_schema
    def get(self, request, pk):
        category = get_category_object(pk=pk)
        serializer = self.CategoryOutputSerializer(category, context={'request':request})
        return Response(serializer.data)
    
class CategoryCreateView(APIView):

    class CategoryOutputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=200)
        post = serializers.HyperlinkedRelatedField(view_name='post-detail', read_only=True)
        posts_number = serializers.IntegerField(default=0)

    class CategoryInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=200)
        description = serializers.CharField(max_length=500,)

    permission_classes = [IsAdminUser]

    @category_create_schema
    def post(self, request):
        serializer = self.CategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = category_create(data=serializer.validated_data)
        output = self.CategoryOutputSerializer(category, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

class CategoryUpdateView(APIView):


    class CategoryOutputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=200)
        post = serializers.HyperlinkedRelatedField(view_name='post-detail', read_only=True)
        posts_number = serializers.IntegerField(default=0)

    class CategoryInputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=200)
        description = serializers.CharField(max_length=500,)

    permission_classes = [IsAdminUser]

    @category_update_schema
    def put(self, request, pk):
        category = get_category_object(pk=pk)
        serializer = self.CategoryInputSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        category = category_update(category=category, data=serializer.validated_data)
        output = self.CategoryOutputSerializer(category, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

    @category_update_schema
    def patch(self, request, pk):
        category = get_category_object(pk=pk)
        serializer = self.CategoryInputSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        category = category_update(category=category, data=serializer.validated_data)
        output = self.CategoryOutputSerializer(category, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

class CategoryDeleteView(APIView):

    permission_classes = [IsAdminUser]

    @category_delete_schema
    def delete(self, request, pk):
        category = get_category_object(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        
