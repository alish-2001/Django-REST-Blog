from rest_framework.urls import path
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView

from .views import UserCreateView, UserLoginView, UserProfileView, UsersListView, UserLogoutView, UserVerifyAccount

urlpatterns = [

    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('users/', UsersListView.as_view(), name='users-list'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('verify-account/', UserVerifyAccount.as_view(), name='user-verify-account'),

]
