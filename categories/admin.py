from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = (
        "name",
        "description",
    )

    list_display = (
        "id",
        "name",
        "description",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "name",
    )

    list_per_page = 20
