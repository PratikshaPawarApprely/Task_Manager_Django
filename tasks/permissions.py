
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


class TaskPermission(BasePermission):
    """
    Viewer:
        Read-only access.

    Contributor:
        Read tasks, create tasks, and update own tasks.

    Admin:
        Full access to all tasks.
    """

    def has_permission(self, request, view):
        role = get_user_role(request.user)

        # Reject users without a valid application role.
        if role is None:
            return False

        # All roles can read tasks.
        if request.method in SAFE_METHODS:
            return True

        # Admin can perform every write operation.
        if role == "admin":
            return True

        # Contributor can create tasks.
        if role == "contributor" and request.method == "POST":
            return True

        # Contributor can attempt updates, subject to
        # the object-level ownership check below.
        if role == "contributor" and request.method in ["PUT", "PATCH"]:
            return True

        # Viewers cannot write. Contributors cannot delete.
        return False

    def has_object_permission(self, request, view, obj):
        role = get_user_role(request.user)

        # Admin can manage any task.
        if role == "admin":
            return True

        # Viewer and Contributor can read any task.
        if request.method in SAFE_METHODS:
            return role in ["viewer", "contributor"]

        # Contributors can update only tasks they created.
        if role == "contributor":
            if request.method in ["PUT", "PATCH"]:
                return obj.created_by_id == request.user.id

        # All other write operations are denied.
        return False
