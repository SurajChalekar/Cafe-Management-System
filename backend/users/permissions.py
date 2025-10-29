from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to staff users (staff or admin).
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff_member())


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Object-level permission: staff can access any user, customer only their own data.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff_member():
            return True
        return obj == request.user
