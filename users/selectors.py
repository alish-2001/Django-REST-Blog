from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model


User = get_user_model()

def get_user_object(pk:int):
    return get_object_or_404(User, pk=pk)

def get_users_queryset():
    return User.objects.all()
