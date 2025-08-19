from rest_framework.viewsets import ViewSet,ModelViewSet,GenericViewSet
from django.db.models import Count
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Post,Comment,Category
from .serializers import PostSerializer,CommentSerializer,CategorySerializer,CategoryDetailSerializer

class PostViewSet(ModelViewSet):

    serializer_class = PostSerializer

    def get_queryset(self):
        queryset = Post.objects.filter(status='pub').select_related('category','user').prefetch_related('likes').all()
        return queryset
    
    def get_serializer_context(self):

        user = self.request.user.id
        
        return {'user':user,}
     

class CommentViewSet(ModelViewSet): 

    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_pk']
        qs = Comment.objects.filter(post_id=post_id, status='a').select_related('user','post').all()
        return qs
    
    def get_serializer_context(self):
        return {'post_pk': self.kwargs['post_pk'], 'user_id': self.request.user.id}
#a view to show category list,category detail and number of related posts to a category

class CategoryViewSet(ViewSet):

    def list(self, request):
        queryset = Category.objects.annotate(category_posts_count=Count('posts')).all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        obj = get_object_or_404(Category.objects.prefetch_related('posts'), id=pk)
        serializer = CategoryDetailSerializer(obj,context={'request':request})
        return Response(serializer.data)    
