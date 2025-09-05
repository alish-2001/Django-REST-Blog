import random
from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTPVerification
from .selectors import check_user_existence
from .validations import validate_user_create

User = get_user_model()

@transaction.atomic
def user_create(*, data:dict):

    email = data.get("email")
    password = data.get("password")

    validate_user_create(data=data)

    user = User.objects.create_user(email=email, password=password)

    try:
        user.full_clean()
    except ValidationError as errors:
        raise ValidationError(errors.messages)

    try:
        otp_create(user)
    except ValidationError as errors:
        raise ValidationError(errors.messages)
    
    return user

def otp_create(user):

    if not check_user_existence(user.email):
        raise ValidationError("User Is NOT Registered")
    
    code = str(random.randint(10000, 99999))
    expired_at = timezone.now() + timedelta(minutes=5)
    otp_obj = OTPVerification(code=code, user=user, expired_at=expired_at)

    with transaction.atomic():
        try:
            otp_obj.full_clean()
            otp_obj.save()
        except ValidationError as errors:
            raise ValidationError(errors.messages_dict)
        
        transaction.on_commit(lambda: send_otp_email(user=otp_obj.user, code=otp_obj))

    return otp_obj

@transaction.atomic
def verify_user_by_otp(user):

    try:
        user = User.objects.get(pk=user.id)
    except User.DoesNotExist:
        raise ("User Not Found")

    user.is_verified = True
    user.save(update_fields=["is_verified"])

    return user

@transaction.atomic
def token_create(user):

    if not check_user_existence(user.email) or user is None:
        raise ValueError("Prepare A Valid User")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def send_otp_email(*, user, otp_obj):

    context = {"code": otp_obj.code, "site_name":"Blog Team", "expiry_minutes":"5",}
    text_content = render_to_string("emails/verification_email.txt", context)

    send_mail(
        "Verify Your Account",
        text_content,
        None,
        [user.email],

    )
