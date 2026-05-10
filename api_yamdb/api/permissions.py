from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

class IsAuthorOrReadOnly(BasePermission):
    """
    Разрешает безопасные методы всем (даже анонимам).
    Создание — только аутентифицированным.
    Изменение и удаление — автору, модератору или администратору.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user:
            return True
        return (
            request.user.role in ('moderator', 'admin')
            or request.user.is_superuser
        )