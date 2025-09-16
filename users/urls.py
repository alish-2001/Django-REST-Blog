from rest_framework.urls import path

from .views import UserCreateView, UserLoginView, UserProfileView, UserTokenRefreshView, UserTokenVerifyView, UsersListView, UserLogoutView, UserVerifyAccount

urlpatterns = [

    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/', UsersListView.as_view(), name='users-list'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('verify-account/', UserVerifyAccount.as_view(), name='user-verify-account'),
    path('token/refresh/', UserTokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', UserTokenVerifyView.as_view(), name='token-verify'),


]
