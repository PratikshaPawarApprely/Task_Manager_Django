from django.db.models import Q


def filter_projects(queryset, params):
    search = params.get("search")
    ordering = params.get("ordering")

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    if ordering:
        queryset = queryset.order_by(ordering)

    return queryset
