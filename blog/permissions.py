from rest_framework.permissions import BasePermission,SAFE_METHODS

UNSAFE_METHODS = ['DELETE', 'PUT', 'PATCH']

class IsPostAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS : 
            return True
        elif request.method in UNSAFE_METHODS:
            return (request.user.is_authenticated and request.user == obj.user) or request.user.is_staff


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS : 
            return True
        return request.user.is_authenticated and request.user.is_staff
    