from rest_framework import serializers, validators
from django.contrib.auth.password_validation import validate_password

class UserCreateSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True, write_only=True, max_length=60)
    password = serializers.CharField(required=True, write_only=True, max_length=50, validators=[validate_password])
    confirm_password = serializers.CharField(required=True, write_only=True, max_length=50)

class UserOutputSerializer(serializers.Serializer):

    email = serializers.EmailField(read_only=True)
    