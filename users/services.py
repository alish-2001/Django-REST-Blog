import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError, NotFound
from django.conf import settings

from .models import OTPVerification
from .selectors import check_user_existence
from .validations import validate_request_otp, validate_user_create

User = get_user_model()

def user_create(*, data:dict):

    cleaned_data = validate_user_create(data=data)
    email = cleaned_data.get("email")
    password = cleaned_data.get("password")

    user = User(email=email, username=email)
    user.set_password(password)

    try:
        user.full_clean()
    except DjangoValidationError as e:
        raise DRFValidationError(str(e))

    try:
        with transaction.atomic():
            user.save()
            transaction.on_commit(lambda: otp_create(user=user))

    except  IntegrityError as exc:
        raise DRFValidationError(str(exc))
    
    except DjangoValidationError as e:
        raise DRFValidationError(e.messages)

    except Exception as e:
        raise DRFValidationError('Registration Failed')
    
    return user

def otp_create(user):

    if not check_user_existence(user.email):
        raise NotFound('User Is Not Registered')

    #ToDo: storing codes hashed 
    code = str(random.randint(10000, 99999))
    expired_at = timezone.now() + timedelta(minutes=5)

    with transaction.atomic():

        otp_obj = OTPVerification(code=code, user=user, expired_at=expired_at)

        try:
            otp_obj.full_clean()
        except DjangoValidationError as errors:
            raise DRFValidationError(errors.messages_dict)
        
        try:
            otp_obj.save()
        except Exception:
            raise DRFValidationError('Failded To Create Verification Code')

        transaction.on_commit(lambda: send_otp_email(user=otp_obj.user, otp_obj=otp_obj))

    return otp_obj

@transaction.atomic
def verify_user_by_otp(user):

    if getattr(user, 'is_verified', False):
        raise DRFValidationError('Account Is Already Verified')
    
    updated = User.objects.filter(pk=user.id, is_verified=False).update(is_verified=True)

    if not updated:
        raise DRFValidationError("Account Is Already Verified Or Cannot Be Verified")
    
def token_create(user):


    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def send_otp_email(*, user, otp_obj):

    context = {"otp": otp_obj.code, "site_name":"Negaresh Blog", "expiry_minutes":"5",}
    text_content = render_to_string("emails/verification_email.txt", context)
    html_content = render_to_string("emails/verification_email.html", context)

    try:
        msg = EmailMultiAlternatives(
        "Verify your account",
        text_content,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except:
        raise DRFValidationError("Sending OTP Faild")

def request_otp(email):
    
    user = validate_request_otp(email)
    otp = otp_create(user=user)
    return otp
