
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import transaction


ROLE_NAMES = {"Viewer", "Contributor", "Admin"}


@transaction.atomic
def assign_user_role(user, role_name="Viewer"):
    if role_name not in ROLE_NAMES:
        raise ValidationError("Invalid role name.")

    role_group = Group.objects.get(name=role_name)

    # Remove previous application roles.
    user.groups.remove(
        *user.groups.filter(name__in=ROLE_NAMES)
    )

    # Assign the new role.
    user.groups.add(role_group)

    return user
