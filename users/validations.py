from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

from .selectors import get_latest_user_otp_obj, get_user_object, check_user_existence

User = get_user_model()

def validate_user_create(data:dict):

    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not email or not password or not confirm_password:
        raise ValidationError("All The Fields Are Required")
    
    email = BaseUserManager.normalize_email(email=email)

    try:
        validate_email(email)
    except:
        raise ValidationError("Please enter A Valid Email Address ")

    if  password != confirm_password:
        raise ValidationError("Passwords Do Not Match")   
     
    try:
        validate_password(password=password)
    except Exception as error:
        raise ValidationError({'errors':list(error.messages)})

    if check_user_existence(email=email):
        raise ValidationError("This Email Address Is Registered")

    return None

def validate_user_authentication(data:dict):


    email = (data.get("email"))
    password = data.get("password")
    
    if not email or not password:
        raise ValidationError("Email And Password Are Required")

    email = BaseUserManager.normalize_email(email=email.strip())

    user = authenticate(username=email, password=password)

    if not user:
        raise ValidationError("Invalid Email Or Password.")

    if not user.is_active:
        raise ValidationError("This account is disabled.")
    
    if not getattr(user, "is_verified", False):
        raise ValidationError("This account is not verified.")
    
    return user

def validate_otp_new_authenticated_user(*, user, code:str):


    if not code or not user:
        raise ValidationError("Input Code or Other required Data NOT Found")

    if len(code) >= 6 or not code.isdecimal():
        raise ValidationError("input Code Is NOT Correct")

    try:
        user = get_user_object(pk=user.pk)
    except User.DoesNotExist:
        raise ("invalid User or Code")
    
    if  not user.is_authenticated:
        raise ValidationError("User Is Not Logged In")

    if user.is_verified:
        raise ValidationError("Account Is Already Verfied")

    try:
        otp_obj = get_latest_user_otp_obj(user=user)
    except Exception:
        raise ValidationError("No Code Is Sent For This Account")

    if otp_obj.is_expired:
        raise ValidationError("Code Is Expired. Try Another Time")

    if otp_obj.code != code:
        raise ValidationError("Input Code Is Not Correct")

    return None

def validate_otp_new_anonymous_user(*, code:str, user_id:int):
    
    if not code or not user_id:
        raise ValidationError("All the fields are required")
    
    if len(code) >= 6 or not code.isdecimal():
        raise ValidationError('code format is not correct')

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise ValidationError({"user_id":"Invalid User ID"})

    try:
        user = get_user_object(pk=user_id)
    except User.DoesNotExist:
        raise ("invalid User or Code")
    

    if user.is_verified:
        raise ValidationError("Account is Already Verified")


    try:
        otp_obj = get_latest_user_otp_obj(user=user)
    except Exception:
        raise ValidationError("No code found for the given user")

    if otp_obj.is_expired():
        raise ValidationError('Code is Expired, Request Another Time')

    if otp_obj.code != code:
        raise ValidationError("entered code is not correct")
        
    return None
