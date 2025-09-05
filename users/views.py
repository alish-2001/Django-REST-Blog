from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from .selectors import get_user_object, get_users_queryset
from .services import verify_user_by_otp, user_create, token_create
from .validations import validate_otp_new_authenticated_user, validate_user_authentication, validate_otp_new_anonymous_user
from .serializers import UserCreateInputSerializer, UserLoginInputSerializer, UserCreateOutputSerializer, UserLoginOutputSerializer, UserLogoutInputSerializer, UserProfileOutputSerializer, UserVerifyAccountInputSerializer, UsersListSerializer

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

        user = validate_user_authentication(data=serializer.validated_data)

        if not user:
            raise ValidationError("Invalid Email or Password")

        tokens = token_create(user=user)
        
        output = {

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

    def get(self, request):
           
        user = get_user_object(pk=request.user.id)
        serializer = UserProfileOutputSerializer(user, context={'request':request})
        return Response(serializer.data)

class UsersListView(APIView):
    
    permission_classes = [IsAdminUser]

    def get(self, request):

        users= get_users_queryset()
        serializer = UsersListSerializer(users, many=True, context={'request':request})
        return Response(serializer.data)

class UserLogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = UserLogoutInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh = serializer.validated_data['refresh']
            token =  RefreshToken(refresh)
            token.blacklist()
            return Response({'message':'User Logged out Successfuly'}, status=status.HTTP_205_RESET_CONTENT)
        
        except TokenError as error:
            return Response({'detail': f"Invalid refresh token for {request.user.username}: {str(error)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class UserVerifyAccount(APIView):

    def post(self, request):
        
        serializer = UserVerifyAccountInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        code = serializer.validated_data['code']

        try:
            #If user exists, but not logged in (without a valid token)
            if  request.user.is_authenticated:
                    user = request.user
                    validate_otp_new_authenticated_user(user=user, code=code)
                    verify_user_by_otp(user)
                    return Response({'message':'User Verified Successfully'}, status=status.HTTP_200_OK)
                
            #If user exists, but is anonymous(not logged in), get user ID which is sent from client request, to verify user
            else:                 
                    user_id = request.data.get('user_id')
                    validate_otp_new_anonymous_user(code=code, user_id=user_id)
                    user = get_user_object(pk=user_id)
                    verify_user_by_otp(user=user)
                    return Response({'message':'User Verified Successfully'}, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        