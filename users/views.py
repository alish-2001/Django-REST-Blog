from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

from .serializers import UserCreateSerializer,UserOutputSerializer
from .services import user_create

# Create your views here.

class UserCreateView(APIView):

    def post(self, request):
       
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid()
        user = user_create(data=serializer.validated_data)
        return Response(UserOutputSerializer(user).data, status=status.HTTP_201_CREATED)
    
    