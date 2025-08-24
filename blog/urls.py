from rest_framework_nested import routers
from rest_framework.urls import path

from .views import CategoryView, PostUpdateView,PostCommentView,PostListView,PostDetailView,PostDeleteView,PostCreateView


urlpatterns=[
    path('posts/',PostListView.as_view(), name='posts'),
    path('posts/create',PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/comments/', PostCommentView.as_view(), name='post-comments'),
    path('categories/', CategoryView.as_view(), name='categories'),
]


# router=routers.DefaultRouter()

# router.register('posts', PostViewSet, basename='post')

# router.register('categories',CategoryViewSet,basename='category')

# post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
# post_router.register('comments', viewset=CommentViewSet, basename='post-comments')

# urlpatterns = router.urls + post_router.urls
