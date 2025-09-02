from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

def user_create_validate(data:dict):

    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")

    if not email or not password or not confirm_password:
        return ValidationError("All the fields are required")

  
    if  password != confirm_password:
        raise ValidationError("Passwords Do Not Match")   
     
    try:
        validate_email(email)
    except:
        raise ValidationError("Please enter a valid email address ")


    try:
        validate_password(password=password)
    except Exception as error:
        raise ValidationError({'errors':list(error.messages)})


    if User.objects.filter(email=email).exists():
        return ValidationError("This email address is registered")
