from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    model = User
    list_display = ['id','username','email', 'role', 'is_verified']
    