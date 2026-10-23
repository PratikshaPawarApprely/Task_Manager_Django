from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project

        fields = [
            "id",
            "name",
            "description",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]

    def validate_name(self, value):

        if not value:
            raise serializers.ValidationError(
                "Project name is required."
            )

        if not isinstance(value, str):
            raise serializers.ValidationError(
                "Project name must be a string."
            )

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Project name must contain at least 3 characters."
            )

        return value.strip()
