from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, OTPVerification
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['id','username','email', 'role', 'is_verified']
    readonly_fields = ['created_at','updated_at']

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):

    list_display = ['id','user','code', 'expired_at', 'verification_type', 'created_at']
    readonly_fields = ['created_at','updated_at']
