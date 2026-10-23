
from rest_framework import viewsets
from .models import Project
from .project_serializer import ProjectSerializer
from .filters import filter_projects
from .permissions import AdminOrReadOnly


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [
        AdminOrReadOnly
    ]

    def get_queryset(self):
        queryset = super().get_queryset()

        return filter_projects(
            queryset,
            self.request.query_params
        )
