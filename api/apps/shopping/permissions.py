from rest_framework.permissions import BasePermission


class IsAuthenticatedOrSuperUserForDelete(BasePermission):
    """Custom permission:
    - DELETE: Only authenticated superusers.
    - Other methods: Allowed for any authenticated user.
    """

    def has_permission(self, request, view) -> bool:
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if request.method == "DELETE":
            return user.is_superuser

        return True
