
from rest_framework.permissions import BasePermission, SAFE_METHODS


ROLE_NAMES = {
    "Viewer": "viewer",
    "Contributor": "contributor",
    "Admin": "admin",
}


def get_user_role(user):
    if not user or not user.is_authenticated:
        return None

    roles = list(
        user.groups.filter(
            name__in=ROLE_NAMES.keys()
        ).values_list("name", flat=True)
    )

    # A user must have exactly one application role.
    if len(roles) != 1:
        return None

    return ROLE_NAMES[roles[0]]


class AdminOrReadOnly(BasePermission):
    """
    All assigned roles can read.
    Only Admin can create, update, or delete.
    """

    def has_permission(self, request, view):
        role = get_user_role(request.user)

        if request.method in SAFE_METHODS:
            return role in ["viewer", "contributor", "admin"]

        return role == "admin"
