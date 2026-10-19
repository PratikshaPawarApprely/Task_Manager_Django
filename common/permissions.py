from rest_framework.permissions import BasePermission, SAFE_METHODS


def get_user_role(user):
    if not user or not user.is_authenticated:
        return None

    profile = getattr(user, "profile", None)
    return getattr(profile, "role", None)


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        role = get_user_role(request.user)

        if request.method in SAFE_METHODS:
            return role in ["viewer", "contributor", "admin"]

        return role == "admin"


class IsViewer(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == "viewer"


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == "contributor"


class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == "admin"


class TaskPermission(BasePermission):

    def has_permission(self, request, view):
        role = get_user_role(request.user)

        if role not in ["viewer", "contributor", "admin"]:
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            return role in ["contributor", "admin"]

        return role in ["contributor", "admin"]

    def has_object_permission(self, request, view, obj):
        role = get_user_role(request.user)

        if role == "admin":
            return True

        if request.method in SAFE_METHODS:
            return role in ["viewer", "contributor"]

        if role == "contributor":
            return obj.created_by_id == request.user.id

        return False