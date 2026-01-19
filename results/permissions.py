from rest_framework import permissions


class is_principal(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.is_teacher or request.user.is_principal
    
