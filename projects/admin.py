from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "description",
    )

    list_display = (
        "id",
        "name",
        "description",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 20

    readonly_fields = (
        "created_at",
    )
