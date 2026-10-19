
from rest_framework import viewsets

from .models import Task
from .task_serializer_v2 import TaskSerializerV2
from .filters import filter_tasks
from .permissions import TaskPermission
from common.pagination import CustomPagination


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
