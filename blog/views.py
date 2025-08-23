from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from rest_framework.views import APIView

from .serializers import CategoryInputSerializer, CategoryOutputSerializer, CommentInputSerializer, CommentOutputSerializer, PostInputSerializer, PostOutputSerializer
from .services import category_create, post_create,comment_create,post_update
from .selectors import get_post_queryset,get_post_object,get_post_comment_queryset,get_category_queryset
from .permissions import IsPostAuthorOrReadOnly,IsStaffOrReadOnly


class PostDetailView(RetrieveAPIView):

    serializer_class = PostOutputSerializer
    
    def get_queryset(self):
        return get_post_queryset()


    #def get for any, put and patch for author

class CategoryView(ListCreateAPIView):

    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        return get_category_queryset()

    def get_serializer_class(self):

        if self.request.method == "GET":
            return CategoryOutputSerializer
        elif self.request.method == "POST":
            return CategoryInputSerializer

    def create(self, request, *args, **kwargs):

        serializer = CategoryInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = category_create(data=serializer.validated_data, user=request.user)
        output = CategoryInputSerializer(category, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

class PostDeleteView(APIView):

    permission_classes = [IsPostAuthorOrReadOnly]

    def get_object(self):
        return get_post_object(pk=self.kwargs['pk'])
    
    def get(self, request, pk):
        post =self.get_object() 
        serializer = PostOutputSerializer(post, context={'request':request})
        return Response(serializer.data)

    def delete(self, request, pk):
        post = self.get_object()
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)        
       
class PostListView(APIView):

    permission_classes = [IsStaffOrReadOnly]

    def get(self, request):
        posts = get_post_queryset() 
        serializer = PostOutputSerializer(posts, context={'request':request}, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post = post_create(data=serializer.validated_data, user=request.user)
        output = PostInputSerializer(post, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

class PostCommentView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        
        comments = get_post_comment_queryset(pk=pk) 
        serializer = CommentOutputSerializer(comments, context={'request':request}, many=True)
        return Response(serializer.data)

    def post(self,request,pk):
        
        post = get_post_object(pk=pk)
        serializer = CommentInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = comment_create(post=post, data=serializer.validated_data, user=request.user) 
        return Response(CommentOutputSerializer(comment, context={'request':request}).data, status=status.HTTP_201_CREATED)

class PostUpdateView(APIView):

    permission_classes = [IsPostAuthorOrReadOnly]

    def get_object(self):
        return get_post_object(pk=self.kwargs['pk'])
    
    
    def get(self, request, pk):
        post =self.get_object() 
        serializer = PostOutputSerializer(post, context={'request':request})
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object()
        serializer = PostInputSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        post = post_update(post=post, data=serializer.validated_data, user=request.user)
        output = PostOutputSerializer(post, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        post = self.get_object()
        serializer = PostInputSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        post = post_update(post=post, data=serializer.validated_data, user=request.user)

        output = PostOutputSerializer(post, context={"request": request})
        return Response(output.data, status=status.HTTP_200_OK)


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
