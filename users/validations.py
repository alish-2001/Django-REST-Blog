from django.core.validators import validate_email
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import NotFound as DRFNotFound
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError,NotAuthenticated,PermissionDenied

from .selectors import get_latest_user_otp_obj, get_user_object_by_email, get_user_object_by_pk, check_user_existence

User = get_user_model()

def validate_user_create(data:dict):

    email = str(data.get("email")).strip()
    password = str(data.get("password")).strip()
    confirm_password = str(data.get("confirm_password")).strip()

    if not email or not password or not confirm_password:
        raise DRFValidationError("All The Fields Are Required")
    
    email = BaseUserManager.normalize_email(email=email)

    try:
        validate_email(email)
    except DjangoValidationError:
        raise DRFValidationError("Please enter A Valid Email Address ")

    if  password != confirm_password:
        raise DRFValidationError("Passwords Do Not Match")   
     
    try:
        validate_password(password=password)
    except DjangoValidationError as error:
        raise DRFValidationError(str(error))

    if check_user_existence(email=email):
        raise DRFValidationError("This Email Address Is Registered")

    return {'email':email, 'password':password}

def validate_user_authentication(data:dict):

    email = str(data.get("email")).strip()
    password = str(data.get("password")).strip()
    
    if not email or not password:
        raise DRFValidationError("Email And Password Are Required")

    email = BaseUserManager.normalize_email(email=email)

    user = authenticate(username=email, password=password)

    if not user:
        raise NotAuthenticated("This Account Is Not Registered.")

    if not user.is_active:
        raise PermissionDenied("This account is disabled.")
    
    if not getattr(user, "is_verified", False):
        raise PermissionDenied("This account is not verified.")
    
    return user

def validate_otp_new_authenticated_user(*, user, code:str):

    if not code or not user:
        raise DRFValidationError("Input Code or Other required Data NOT Found")

    if len(code) >= 6 or not code.isdecimal():
        raise DRFValidationError("input Code Is NOT Correct")

    try:
        user = get_user_object_by_pk(pk=user.pk)
    except DjangoValidationError:
        raise DRFValidationError("invalid User or Code")
    
    if  not user.is_authenticated:
        raise DRFNotFound("User Is Not Logged In")

    if user.is_verified:
        raise DRFValidationError("Account Is Already Verfied")

    try:
        otp_obj = get_latest_user_otp_obj(user=user)
    except DjangoValidationError:
        raise DRFValidationError("No Code Is Sent For This Account")

    if otp_obj.is_expired:
        raise DRFValidationError("Code Is Expired. Try Another Time")

    if otp_obj.code != code:
        raise DRFValidationError("Input Code Is Not Correct")

    return None

def validate_otp_new_anonymous_user(*, code:str, email):

    if not code or not email:
        raise DRFValidationError("All the fields are required")
    
    if len(code) != 5 or not code.isdecimal():
        raise DRFValidationError('code format is not correct')
    
    code = str(code).strip()
    email = str(email).strip()

    email = BaseUserManager.normalize_email(email)

    try:
        validate_email(email)
    except DjangoValidationError:
        raise DRFValidationError("Please enter A Valid Email Address ")

    try:
        user = get_user_object_by_email(email=email)
    except DRFNotFound:
        raise DRFNotFound("invalid User or Code")
    
    if user.is_verified:
        raise DRFValidationError("Account is Already Verified")

    try:
        otp_obj = get_latest_user_otp_obj(user=user)
    except DRFNotFound as e:
        raise DRFNotFound(str(e))


    if otp_obj.is_expired:
        raise DRFValidationError('Code is Expired, Request Another Time')

    if otp_obj.code != code:
        raise DRFValidationError("entered code is not correct")
        
    return user



