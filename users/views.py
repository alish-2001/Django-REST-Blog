from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

from users.validations import user_authenticate_status
from .serializers import UserCreateInputSerializer, UserLoginInputSerializer,UserCreateOutputSerializer, UserLoginOutputSerializer
from .services import user_create, token_create

# Create your views here.

class UserCreateView(APIView):

    def post(self, request):
       
        serializer = UserCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_create(data=serializer.validated_data)
        return Response(UserCreateOutputSerializer(user, context={'request':request}).data, status=status.HTTP_201_CREATED)
    