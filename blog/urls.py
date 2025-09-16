from rest_framework.urls import path

from .views import CategoryCreateView, CategoryDeleteView, CategoryDetailView, CategoryUpdateView, CommentCreateView, CommentDeleteView, CommentListView, LikeCreateView, PostUpdateView,PostListView,PostDetailView,PostDeleteView,PostCreateView,CategoryListView

urlpatterns=[
    
    path('posts/',PostListView.as_view(), name='posts'),
    path('posts/create',PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    path('posts/<int:pk>/comments/', CommentListView.as_view(), name='comments'),
    path('posts/<int:pk>/comments/create', CommentCreateView.as_view(), name='comment-create'),
    path('posts/<int:post_pk>/comments/<int:comment_pk>/delete', CommentDeleteView.as_view(), name='comment-delete'),

    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/create', CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),

    path('posts/<int:pk>/like/', LikeCreateView.as_view(), name='post-like'),
    
]
