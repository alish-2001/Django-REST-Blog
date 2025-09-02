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
    
class UserLoginView(APIView):

    def post(self, request):

        serializer = UserLoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_authenticate_status(data=serializer.validated_data)

        if not user:
            raise ValidationError("Invalid Username OR Password")

        tokens = token_create(user=user)
        
        output = {
            'request': request,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'access': tokens['access'],
            'refresh': tokens['refresh'],           
        }

        output_serialzier = UserLoginOutputSerializer(output, context={'request': request})
        return Response(output_serialzier.data, status=status.HTTP_200_OK)


