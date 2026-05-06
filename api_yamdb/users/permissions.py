from rest_framework import permissions


class ReadOnlyOrAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class IsAuthorOrModeratorOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        return request.user.role in ('moderator', 'admin') or request.user.is_superuser


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )
