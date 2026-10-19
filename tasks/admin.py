
from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "priority",
        "status",
        "assigned_to",
        "created_by",
        "project",
        "category",
        "due_date",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "assigned_to__username",
        "created_by__username",
        "project__name",
        "category__name",
    )

    list_filter = (
        "priority",
        "status",
        "project",
        "category",
        "created_at",
        "due_date",
    )

    autocomplete_fields = (
        "assigned_to",
        "created_by",
        "project",
        "category",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Task Information",
            {
                "fields": (
                    "title",
                    "description",
                    "priority",
                    "status",
                )
            },
        ),
        (
            "Assignment",
            {
                "fields": (
                    "assigned_to",
                    "created_by",
                    "project",
                    "category",
                )
            },
        ),
        (
            "Schedule",
            {
                "fields": (
                    "due_date",
                    "created_at",
                )
            },
        ),
    )

    ordering = ("-created_at",)

    list_per_page = 20
