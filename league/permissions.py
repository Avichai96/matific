# permissions.py

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission that allows full access to admin users, and read-only access
    to coach and player users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and (request.user.is_admin or request.user.is_coach or request.user.is_player)
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrCoach(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin or request.user.is_coach)


class IsAdminStaff(permissions.BasePermission):
    """
    Allows access only to admin users who are also marked as staff.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin and request.user.is_staff
