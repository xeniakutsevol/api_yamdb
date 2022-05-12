from rest_framework import permissions


class UserAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.role == 'admin'
