from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser,IsAuthenticated

from .permissions import IsPostAuthor
from .services import category_create, category_update, like_create, post_create,comment_create,post_update
from .selectors import get_comment_object, get_post_queryset,get_post_object,get_comment_queryset,get_category_queryset,get_category_object
from .serializers import CategoryInputSerializer, CategoryOutputSerializer, CommentInputSerializer, CommentOutputSerializer, PostInputSerializer, PostOutputSerializer

class PostListView(APIView):
    
    def get(self, request):
        posts = get_post_queryset() 
        serializer = PostOutputSerializer(posts, context={'request':request}, many=True)
        return Response(serializer.data)

class PostCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = post_create(data=serializer.validated_data, user=request.user)
        output = PostInputSerializer(post, context={"request": request})
        return Response(output.data, status=status.HTTP_201_CREATED)

class PostDetailView(APIView):

    def get(self, request, pk):
        post = get_post_object(pk=pk)
        serializer = PostOutputSerializer(post, context={'request':request})
        return Response(serializer.data)

class PostUpdateView(APIView):

    permission_classes = [IsPostAuthor]

    def put(self, request, pk):

        post = get_post_object(pk=pk)
        self.check_object_permissions(request, post)
        serializer = PostInputSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        post = post_update(post=post, data=serializer.validated_data, user=request.user)
        output = PostOutputSerializer(post, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

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

    def delete(self, request, pk):
        post = get_post_object(pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

class CategoryListView(APIView):

    def get(self,request):
        categories = get_category_queryset() 
        serializer = CategoryOutputSerializer(categories, context={'request':request}, many=True)
        return Response(serializer.data)

class CategoryDetailView(APIView):

    def get(self, request, pk):
        category = get_category_object(pk=pk)
        serializer = CategoryOutputSerializer(category, context={'request':request})
        return Response(serializer.data)
    
class CategoryCreateView(APIView):

    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = category_create(data=serializer.validated_data)
        output = CategoryOutputSerializer(category, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

class CategoryUpdateView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        category = get_category_object(pk=pk)
        serializer = CategoryInputSerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        category = category_update(category=category, data=serializer.validated_data)
        output = CategoryOutputSerializer(category, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        category = get_category_object(pk=pk)
        serializer = CategoryInputSerializer(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        category = category_update(category=category, data=serializer.validated_data)
        output = CategoryOutputSerializer(category, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

class CategoryDeleteView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        category = get_category_object(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

class CommentListView(APIView):

    def get(self, request, pk):

        comments = get_comment_queryset(pk=pk) 
        serializer = CommentOutputSerializer(comments, context={'request':request}, many=True)
        return Response(serializer.data)

class CommentCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        
        post = get_post_object(pk=pk)
        serializer = CommentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = comment_create(post=post, data=serializer.validated_data, user=request.user) 
        return Response(CommentOutputSerializer(comment, context={'request':request}).data, status=status.HTTP_201_CREATED)

class CommentDeleteView(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, post_pk, comment_pk):
        comment = get_comment_object(post_pk=post_pk, comment_pk=comment_pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  

class LikeCreateView(APIView):
   
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        post = get_post_object(pk=pk)
        user = request.user
        like_create(post=post, user=user)
        return Response(status=status.HTTP_201_CREATED)
    