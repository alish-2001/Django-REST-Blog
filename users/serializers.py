from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

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

class UserLoginInputSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True, max_length=60)
    password = serializers.CharField(required=True, write_only=True, max_length=50,)

class UserLoginOutputSerializer(serializers.Serializer):
    access = serializers.CharField(max_length=600, read_only=True)
    refresh = serializers.CharField(max_length=2000, read_only=True)
    username = serializers.CharField(max_length=60, read_only=True)
    first_name = serializers.CharField(max_length=150, read_only=True)
    last_name = serializers.CharField(max_length=150, read_only=True)
