from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from tasks.views import TaskViewSet
from projects.views import ProjectViewSet
from categories.views import CategoryViewSet
from tasks.views import cached_tasks_demo

# Router
router = DefaultRouter()

router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"categories", CategoryViewSet, basename="category")


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Main application APIs
    path("api/v1/", include(router.urls)),

    # Accounts
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v2/", include("tasks.urls_v2")),
    path(
        "api/v1/cached-tasks-demo/",
        cached_tasks_demo,
        name="cached-tasks-demo",
    ),
    # Swagger
    path(
        "schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
