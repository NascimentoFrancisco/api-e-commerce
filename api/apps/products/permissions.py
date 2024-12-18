from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedAndSuperUserForUnsafeMethods(BasePermission):
    """
    Custom permission:
    - Secure methods (GET): Available to any user (authenticated or not).
    - Unsecure methods (POST, PUT, DELETE): Require the user to be authenticated and superuser.
    """

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )
