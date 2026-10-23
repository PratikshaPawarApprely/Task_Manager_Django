
from rest_framework.routers import DefaultRouter
from .views_v2 import TaskViewSetV2

router = DefaultRouter()

router.register(
    r"tasks",
    TaskViewSetV2,
    basename="task-v2"
)

urlpatterns = router.urls
