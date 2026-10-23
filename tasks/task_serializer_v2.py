
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Task, Project, Category


class TaskSerializerV2(serializers.ModelSerializer):

    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    created_by_username = serializers.CharField(
        source="created_by.username",
        read_only=True,
        allow_null=True
    )

    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    assigned_to_username = serializers.CharField(
        source="assigned_to.username",
        read_only=True,
        allow_null=True
    )

    project_id = serializers.PrimaryKeyRelatedField(
        source="project",
        queryset=Project.objects.all(),
        required=False,
        allow_null=True
    )

    project_name = serializers.CharField(
        source="project.name",
        read_only=True,
        allow_null=True
    )

    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "created_by",
            "created_by_username",
            "assigned_to",
            "assigned_to_username",
            "project_id",
            "project_name",
            "category_id",
            "category_name",
            "title",
            "description",
            "priority",
            "status",
            "created_at",
            "due_date",
        ]

        read_only_fields = [
            "id",
            "created_by",
            "created_by_username",
            "assigned_to_username",
            "project_name",
            "category_name",
            "created_at",
        ]
