
from rest_framework.permissions import BasePermission


ROLE_NAMES = {"Viewer", "Contributor", "Admin"}


def get_user_role(user):
    if not user or not user.is_authenticated:
        return None

    roles = list(
        user.groups.filter(
            name__in=ROLE_NAMES
        ).values_list("name", flat=True)
    )

    # Deny access if no role or multiple roles are assigned.
    if len(roles) != 1:
        return None

    return roles[0].lower()


class IsAdminRole(BasePermission):

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return (
            user.is_superuser
            or get_user_role(user) == "admin"
        )
