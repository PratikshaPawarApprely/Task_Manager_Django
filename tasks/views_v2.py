
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Task
from .task_serializer_v2 import TaskSerializerV2
from .permissions import TaskPermission
from common.pagination import CustomPagination


@extend_schema_view(
    list=extend_schema(operation_id="tasks_v2_list"),
    create=extend_schema(operation_id="tasks_v2_create"),
    retrieve=extend_schema(operation_id="tasks_v2_retrieve"),
    update=extend_schema(operation_id="tasks_v2_update"),
    partial_update=extend_schema(operation_id="tasks_v2_partial_update"),
    destroy=extend_schema(operation_id="tasks_v2_destroy"),
)
class TaskViewSetV2(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializerV2
    pagination_class = CustomPagination
    permission_classes = [TaskPermission]

    def get_queryset(self):
        return Task.objects.select_related(
            "assigned_to",
            "created_by",
            "project",
            "category",
        ).all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
