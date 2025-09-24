from rest_framework import status
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView

from .selectors import get_user_object_by_pk, get_users_queryset
from .services import request_otp, verify_user_by_otp, user_create, token_create, otp_create
from .validations import validate_user_authentication, validate_otp_new_anonymous_user
from .schemas import user_create_schema,user_login_schema,user_profile_schema,users_list_schema,user_logout_schema,user_verify_account_schema,token_refresh_schema,token_verify_schema,user_request_otp_schema

# Create your views here.

class UserCreateView(APIView):

    class UserCreateInputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, write_only=True, max_length=60)
        password = serializers.CharField(required=True, write_only=True, max_length=50, validators=[validate_password])
        confirm_password = serializers.CharField(required=True, write_only=True, max_length=50, validators=[validate_password])

    class UserCreateOutputSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        email = serializers.EmailField(read_only=True)
        role = serializers.CharField(read_only=True,)
        is_verified = serializers.BooleanField(read_only=True,)
        is_staff = serializers.BooleanField(read_only=True,)

    permission_classes = [AllowAny]

    @user_create_schema
    def post(self, request):

        serializer = self.UserCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        user = user_create(data=serializer.validated_data)
        return Response(self.UserCreateOutputSerializer(user, context={'request':request}).data, status=status.HTTP_201_CREATED)
    
class UserLoginView(APIView):

    class UserLoginInputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, write_only=True, max_length=60,)
        password = serializers.CharField(required=True, write_only=True, max_length=50,)

    class UserLoginOutputSerializer(serializers.Serializer):
        access = serializers.CharField(max_length=600, read_only=True)
        refresh = serializers.CharField(max_length=2000, read_only=True)
        username = serializers.CharField(max_length=60, read_only=True)
        first_name = serializers.CharField(max_length=150, read_only=True)
        last_name = serializers.CharField(max_length=150, read_only=True)

    permission_classes = [AllowAny]

    @user_login_schema
    def post(self, request):

        serializer = self.UserLoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = validate_user_authentication(data=serializer.validated_data)

        tokens = token_create(user=user)
        
        output = {

            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'access': tokens['access'],
            'refresh': tokens['refresh'],           
        }

        output_serialzier = self.UserLoginOutputSerializer(output, context={'request': request})
        return Response(output_serialzier.data, status=status.HTTP_200_OK)
    
class UserProfileView(APIView):

    class UserProfileOutputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=60, read_only=True)
        first_name = serializers.CharField(max_length=150, read_only=True)
        last_name = serializers.CharField(max_length=150, read_only=True)
        bio = serializers.CharField(max_length=500, read_only=True)
        gender = serializers.CharField(max_length=10, read_only=True)
        phone_number = serializers.CharField(max_length=15, read_only=True) 
        image = serializers.ImageField(use_url=True, read_only=True, max_length=None)
        birth_date = serializers.DateField(read_only=True)
        is_verified = serializers.BooleanField(read_only=True)

    permission_classes = [IsAuthenticated]

    @user_profile_schema
    def get(self, request):

        user = get_user_object_by_pk(pk=request.user.id)
        serializer = self.UserProfileOutputSerializer(user, context={'request':request})
        return Response(serializer.data)
 
class UsersListView(APIView):
    
    class UsersListSerializer(serializers.Serializer):
        id = serializers.IntegerField(read_only=True)
        username = serializers.CharField(max_length=60, read_only=True) 
        is_active = serializers.BooleanField(read_only=True)
        gender = serializers.CharField(max_length=10, read_only=True)
        role = serializers.CharField(max_length=10, read_only=True)
        is_verified = serializers.BooleanField(read_only=True)
        is_superuser = serializers.BooleanField(read_only=True)

    permission_classes = [IsAdminUser]

    @users_list_schema
    def get(self, request):

        users= get_users_queryset()
        serializer = self.UsersListSerializer(users, many=True, context={'request':request})
        return Response(serializer.data)

class UserLogoutView(APIView):

    class UserLogoutInputSerializer(serializers.Serializer):
        refresh = serializers.CharField(required=True, max_length=2000, write_only=True)

    permission_classes = [IsAuthenticated]

    @user_logout_schema
    def post(self, request):

        serializer = self.UserLogoutInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh = serializer.validated_data['refresh']
            token =  RefreshToken(refresh)
            token.blacklist()
            return Response({'message':'User Logged out Successfuly'}, status=status.HTTP_205_RESET_CONTENT)
        
        except TokenError as error:
            return Response({'detail': f"Invalid refresh token for {request.user.username}: {str(error)}"}, status=status.HTTP_400_BAD_REQUEST)
        
class UserVerifyAccount(APIView):

    class UserVerifyAccountInputSerializer(serializers.Serializer):
        code = serializers.CharField(max_length=5, write_only=True, required=True)
        email = serializers.EmailField(required=True, write_only=True, max_length=60)

    permission_classes = [AllowAny]

    @user_verify_account_schema
    def post(self, request):

        serializer = self.UserVerifyAccountInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   

        code = serializer.validated_data['code']
        email = serializer.validated_data['email'] 
        
        user = validate_otp_new_anonymous_user(code=code, email=email)
        verify_user_by_otp(user=user)
        
        return Response({'message':'User Verified Successfully'}, status=status.HTTP_200_OK)

@token_refresh_schema
class UserTokenRefreshView(TokenRefreshView):
    pass 

@token_verify_schema
class UserTokenVerifyView(TokenVerifyView):
    pass 

class UserRequestOTP(APIView):

    class UserRequestOTPInputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True, write_only=True, max_length=60)

    @user_request_otp_schema
    def post(self, request):

        serializer = self.UserRequestOTPInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        
        request_otp(email=serializer.validated_data['email'])

        return Response({'message':'OTP created successfuly and sent to the email'}, status=status.HTTP_201_CREATED)
    