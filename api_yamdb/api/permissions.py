from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAuthorOrReadOnly(BasePermission):
    """ 
    Разрешает безопасные методы всем пользователям.
    Изменение и удаление доступно только автору, модератору или администратору.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS 
            or obj.author == request.user
            or request.user.is_staff
            or request.user.is_superuser)
    

class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает чтение всем, а запись только админу."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAdmin(permissions.BasePermission):
    """Полный доступ только для администратора."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
