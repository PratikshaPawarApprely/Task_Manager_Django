from django.db.models import Q


def filter_tasks(queryset, params):
    status_value = params.get("status")
    priority = params.get("priority")
    project_id = params.get("project_id")
    category_id = params.get("category_id")
    user_id = params.get("user_id")
    due_date = params.get("due_date")
    search = params.get("search")
    ordering = params.get("ordering")

    if status_value:
        queryset = queryset.filter(status=status_value)

    if priority:
        queryset = queryset.filter(priority=priority)

    if project_id:
        queryset = queryset.filter(project_id=project_id)

    if category_id:
        queryset = queryset.filter(category_id=category_id)

    if user_id:
        queryset = queryset.filter(user_id=user_id)
    if due_date:
        queryset = queryset.filter(due_date=due_date)

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    if ordering:
        queryset = queryset.order_by(ordering)

    return queryset