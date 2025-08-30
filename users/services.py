from django.db import transaction

from .models import User

@transaction.atomic
def user_create(*, is_active: bool = True, is_admin: bool = False, data:dict):
     
    if data['password'] == data['confirm_password']:

        user = User.objects.create_user(
            username=data['email'],
            password=data['password'],
            email=data['email'],
            is_active=is_active,
            is_staff=is_admin,
        )
        return user
    
    