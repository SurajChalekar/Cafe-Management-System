from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    """
    Allows access only to staff or admin users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_staff_member', False))


class IsCustomerUser(permissions.BasePermission):
    """
    Allows access only to customer users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'customer')


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Object-level permission to allow access only to the owner or staff.
    """
    def has_object_permission(self, request, view, obj):
        # Staff can access any object
        if request.user.is_staff_member():
            return True

        # Otherwise, only the owner/customer can access
        if hasattr(obj, 'customer'):
            return obj.customer == request.user
        elif hasattr(obj, 'cart'):
            return obj.cart.customer == request.user
        return False
