
from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Task, Project, Category
from common.choices import Priority, Status


class TaskSerializer(serializers.ModelSerializer):

    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    project_id = serializers.PrimaryKeyRelatedField(
        source="project",
        queryset=Project.objects.all(),
        required=False,
        allow_null=True
    )

    category_id = serializers.PrimaryKeyRelatedField(
        source="category",
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "created_by",
            "assigned_to",
            "project_id",
            "category_id",
            "title",
            "description",
            "priority",
            "status",
            "created_at",
            "due_date",
        ]
        read_only_fields = ["id", "created_by", "created_at"]

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "Title must contain at least 3 characters."
            )

        return value

    def validate_priority(self, value):
        value = value.strip().lower()

        if value not in Priority.values:
            raise serializers.ValidationError(
                "Priority must be low, medium, or high."
            )

        return value

    def validate_status(self, value):
        value = value.strip().lower()

        if value not in Status.values:
            raise serializers.ValidationError(
                "Status must be pending or completed."
            )

        return value

    def validate_due_date(self, value):
        if value is not None and value < timezone.localdate():
            raise serializers.ValidationError(
                "Due date cannot be in the past."
            )

        return value

    def validate(self, attrs):
        status = attrs.get(
            "status",
            getattr(self.instance, "status", None)
        )

        due_date = attrs.get(
            "due_date",
            getattr(self.instance, "due_date", None)
        )

        if (
            status == Status.COMPLETED
            and due_date
            and due_date > timezone.localdate()
        ):
            raise serializers.ValidationError({
                "due_date":
                    "Completed task cannot have a future due date."
            })

        return attrs
