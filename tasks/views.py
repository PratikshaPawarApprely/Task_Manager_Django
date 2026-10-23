from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.core.cache import cache
from rest_framework import viewsets
from .models import Task
from .task_serializer import TaskSerializer
from .filters import filter_tasks
from common.pagination import CustomPagination
from .permissions import TaskPermission


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = CustomPagination
    permission_classes = [TaskPermission]

    def get_queryset(self):
        queryset = super().get_queryset()
        return filter_tasks(queryset, self.request.query_params)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cached_tasks_demo(request):
    cache_key = f"task_manager:tasks:user:{request.user.id}"

    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return Response({
            "source": "redis",
            "data": cached_data,
        })

    queryset = (
        Task.objects
        .filter(created_by=request.user)
        .select_related(
            "project",
            "category",
            "assigned_to",
            "created_by",
        )
        .order_by("id")
    )

    serialized_data = TaskSerializer(
        queryset,
        many=True,
        context={"request": request},
    ).data

    cache.set(cache_key, serialized_data, timeout=300)

    return Response({
        "source": "postgresql",
        "data": serialized_data,
    })
