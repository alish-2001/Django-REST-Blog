from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound as DRFNotFound

from .models import OTPVerification

User = get_user_model()

def get_user_object_by_pk(pk:int):

    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise DRFNotFound("User Not Found")
    
def get_users_queryset():
    return User.objects.all().order_by('-is_active')

def get_latest_user_otp_obj(user):

    otp = OTPVerification.objects.filter(user=user).order_by('-created_at').first()
    if otp is None:
        raise DRFNotFound("No Code Found For This User, Request A New Code.")
    
    return otp

def check_user_existence(email):
    return User.objects.filter(email=email).exists()
