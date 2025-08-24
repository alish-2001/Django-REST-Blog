from rest_framework.permissions import BasePermission,SAFE_METHODS

UNSAFE_METHODS = ['DELETE', 'PUT', 'PATCH']

class IsPostAuthorOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and request.user == obj.user) or (request.user.is_staff)
