
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction

from rest_framework import serializers


User = get_user_model()

ROLE_NAMES = {"Viewer", "Contributor", "Admin"}


# Login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# User details, role, and application permissions
class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    # projects = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "permissions",
            # "projects",
        ]

    def get_role(self, obj):
        roles = list(
            obj.groups.filter(
                name__in=ROLE_NAMES
            ).values_list("name", flat=True)
        )

        if len(roles) == 1:
            return roles[0]

        return None

    def get_permissions(self, obj):
        role = self.get_role(obj)

        permission_map = {
            "Viewer": {
                "can_view_tasks": True,
                "can_create_tasks": False,
                "can_update_own_tasks": False,
                "can_update_all_tasks": False,
                "can_delete_tasks": False,
                "can_manage_users": False,
            },
            "Contributor": {
                "can_view_tasks": True,
                "can_create_tasks": True,
                "can_update_own_tasks": True,
                "can_update_all_tasks": False,
                "can_delete_tasks": False,
                "can_manage_users": False,
            },
            "Admin": {
                "can_view_tasks": True,
                "can_create_tasks": True,
                "can_update_own_tasks": True,
                "can_update_all_tasks": True,
                "can_delete_tasks": True,
                "can_manage_users": True,
            },
        }

        # Users without exactly one recognized role get no permissions.
        return permission_map.get(
            role,
            {
                "can_view_tasks": False,
                "can_create_tasks": False,
                "can_update_own_tasks": False,
                "can_update_all_tasks": False,
                "can_delete_tasks": False,
                "can_manage_users": False,
            },
        )


# Admin creates a user; new users receive Viewer by default.
class CreateUserWithRoleSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        ]
        read_only_fields = ["id"]

    def validate(self, attrs):
        temporary_user = User(
            username=attrs.get("username", ""),
            email=attrs.get("email", ""),
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
        )

        try:
            validate_password(
                attrs["password"],
                user=temporary_user,
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                {"password": list(exc.messages)}
            )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        try:
            viewer_group = Group.objects.get(name="Viewer")
        except Group.DoesNotExist:
            raise serializers.ValidationError(
                {"role": "Viewer group has not been configured."}
            )

        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data,
        )

        user.groups.add(viewer_group)

        return user
