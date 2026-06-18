from rest_framework.permissions import BasePermission, IsAuthenticated


class IsActiveAuthenticated(IsAuthenticated):
    """Allow only authenticated users whose account status is active."""

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return getattr(request.user, 'status', 'active') == 'active'


class IsActiveAdmin(BasePermission):
    """Allow only active authenticated users with the admin role."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and getattr(user, 'status', 'active') == 'active'
            and (
                getattr(user, 'role', None) == 'admin'
                or getattr(user, 'is_staff', False)
                or getattr(user, 'is_superuser', False)
            )
        )
