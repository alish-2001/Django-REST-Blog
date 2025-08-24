from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework import status
from rest_framework.views import APIView

from .serializers import CategoryInputSerializer, CategoryOutputSerializer, CommentInputSerializer, CommentOutputSerializer, PostInputSerializer, PostOutputSerializer
from .services import category_create, category_update, post_create,comment_create,post_update
from .selectors import get_post_queryset,get_post_object,get_post_comment_queryset,get_category_queryset,get_category_object
from .permissions import IsPostAuthorOrReadOnly,IsStaffOrReadOnly

class PostListView(APIView):
    
    def get(self, request):
        posts = get_post_queryset() 
        serializer = PostOutputSerializer(posts, context={'request':request}, many=True)
        return Response(serializer.data)

class PostCreateView(APIView):

    permission_classes = [IsStaffOrReadOnly]

    def post(self, request):
        serializer = PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = post_create(data=serializer.validated_data, user=request.user)
        output = PostInputSerializer(post, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

class PostDetailView(APIView):

    def get(self, request, pk):
        post = get_post_object(pk=pk)
        serializer = PostOutputSerializer(post, context={'request':request})
        return Response(serializer.data)

class PostUpdateView(APIView):

    permission_classes = [IsPostAuthorOrReadOnly]

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
        category = category_create(data=serializer.validated_data, user=request.user)
        output = CategoryOutputSerializer(category, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

class CategoryUpdateView(APIView):

    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        category = get_category_object(pk=pk)
        serializer = CategoryOutputSerializer(category, data=request.data)
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

class PostDeleteView(APIView):

    permission_classes = [IsPostAuthorOrReadOnly]

    def delete(self, request, pk):
        post = get_post_object(pk=pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        

class CommentListView(APIView):

    def get(self, request, pk):

        comments = get_post_comment_queryset(pk=pk) 
        serializer = CommentOutputSerializer(comments, context={'request':request}, many=True)
        return Response(serializer.data)


# class CommentView(APIView):

#     permission_classes = [IsAuthenticatedOrReadOnly]




#Viewsets
# class PostViewSet(ModelViewSet):

#     serializer_class = PostSerializer

#     def get_queryset(self):
#         queryset = Post.objects.filter(status='pub').select_related('category','user').prefetch_related('likes').all()
#         return queryset
    
#     def get_serializer_context(self):

#         user = self.request.user.id
        
#         return {'user':user,}
    
# class CommentViewSet(ModelViewSet): 

#     serializer_class = CommentSerializer

#     def get_queryset(self):
#         post_id = self.kwargs['post_pk']
#         qs = Comment.objects.filter(post_id=post_id, status='a').select_related('user','post').all()
#         return qs
    
#     def get_serializer_context(self):
#         return {'post_pk': self.kwargs['post_pk'], 'user_id': self.request.user.id}

# class CategoryViewSet(ViewSet):

#     def list(self, request):
#         queryset = Category.objects.annotate(category_posts_count=Count('posts')).all()
#         serializer = CategorySerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk):
#         obj = get_object_or_404(Category.objects.prefetch_related('posts'), id=pk)
#         serializer = CategoryDetailSerializer(obj,context={'request':request})
#         return Response(serializer.data)    
