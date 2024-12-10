from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsSuperUserOrReadOnly(BasePermission):
    """Basic authentication class with application-specific customization"""

    def has_permission(self, request, view) -> bool:

        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
            or request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )
