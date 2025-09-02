from django.db import transaction
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError

from .validations import user_create_validate

User = get_user_model()

@transaction.atomic
def user_create(*, data:dict):

    user_create_validate(data)

    email = data.get("email")
    password = data.get("password")


    user = User.objects.create_user(email=email, password=password)

    try:
        user.full_clean()
    except ValidationError as errors:
        raise ValidationError(errors.messages)

    return user
