from rest_framework.urls import path

from .views import UserCreateView, UserLoginView, UserProfileView, UserListView

urlpatterns = [

    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('users/', UserListView.as_view(), name='users-list'),


]
