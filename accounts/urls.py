
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    LoginView,
    ProfileView,
    UserViewSet,
    LogoutView,
    RefreshTokenView,
)

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token-refresh"),
]

urlpatterns += router.urls
