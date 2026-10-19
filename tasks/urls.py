
"""from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = router.urls """

from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import TaskViewSet, cache_demo

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("cached_tasks_demo/", cache_demo, name="cached_tasks_demo"),
] + router.urls