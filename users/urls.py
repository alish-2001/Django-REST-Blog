from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserCreateView, UserLoginView, UserProfileView, UsersListView, UserLogoutView

urlpatterns = [

    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/', UsersListView.as_view(), name='users-list'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),

]
