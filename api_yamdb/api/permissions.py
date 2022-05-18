from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class UserAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'admin' or request.user.is_superuser
                or view.kwargs.get('username') == 'me')


class ReviewCommentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and request.method in [
            'PATCH',
            'DELETE'
        ]:
            return (
                request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
            )
        if request.user.is_authenticated:
            return True


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated and request.user.role == 'admin')
