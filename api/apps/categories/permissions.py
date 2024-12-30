from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsSuperUserOrReadOnly(BasePermission):
    """Basic authentication class with application-specific customization"""

    def has_permission(self, request, view) -> bool:

        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )
