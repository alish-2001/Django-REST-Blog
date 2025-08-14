from rest_framework_nested import routers

from .views import PostViewSet,CommentViewSet,CategoryViewSet

router=routers.DefaultRouter()

router.register('posts', PostViewSet, basename='post')

router.register('categories',CategoryViewSet,basename='category')

post_router = routers.NestedDefaultRouter(router, 'posts', lookup='post')
post_router.register('comments', viewset=CommentViewSet, basename='post-comments')

urlpatterns = router.urls + post_router.urls
