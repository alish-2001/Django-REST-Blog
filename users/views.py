from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .validations import user_authenticate_status
from .serializers import UserCreateInputSerializer, UserLoginInputSerializer,UserCreateOutputSerializer, UserLoginOutputSerializer, UserProfileOutputSerializer, UsersListSerializer
from .services import user_create, token_create
from .selectors import get_user_object, get_users_queryset

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

class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
           
        user = get_user_object(pk=pk)
        serializer = UserProfileOutputSerializer(user, context={'request':request})
        return Response(serializer.data)

class UserListView(APIView):
    
    permission_classes = [IsAdminUser]

    def get(self, request):
        
        users= get_users_queryset()
        serializer = UsersListSerializer(users, many=True, context={'request':request})
        return Response(serializer.data)
    