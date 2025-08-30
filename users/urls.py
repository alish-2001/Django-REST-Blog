from rest_framework.urls import path

from .views import UserCreateView

urlpatterns = [

    path('signup/', UserCreateView.as_view(), name='user-create'),

]