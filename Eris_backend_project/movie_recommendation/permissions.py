from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    # before signin
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.is_superuser:
            return True
        else:
            return False

    # after signup( if user is authenticated, user can't see api that it applied
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return False
        else:
            return True
