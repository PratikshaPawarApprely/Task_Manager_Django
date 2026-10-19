from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category

        fields = [
            "id",
            "name",
            "description",
        ]

        read_only_fields = [
            "id",
        ]

    def validate_name(self, value):

        if not value:
            raise serializers.ValidationError(
                "Category name is required."
            )

        if not isinstance(value, str):
            raise serializers.ValidationError(
                "Category name must be a string."
            )

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Category name must contain at least 3 characters."
            )

        return value.strip()