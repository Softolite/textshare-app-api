from rest_framework import permissions


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access for unauthenticated users
    but require authentication for other actions (e.g., create, update).
    """

    def has_permission(self, request, view):
        # Allow read-only access for unauthenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Require authentication for other actions (e.g., create, update)
        return request.user.is_authenticated
