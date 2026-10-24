
from django.contrib.auth import authenticate, get_user_model

from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema

from .serializers import (
    UserSerializer,
    LoginSerializer,
    CreateUserWithRoleSerializer,
    LoginResponseSerializer,
    LogoutRequestSerializer,
    MessageResponseSerializer,
)
from .permissions import IsAdminRole


User = get_user_model()


# Login
class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
            401: MessageResponseSerializer,
        },
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user is None:
            return Response(
                {
                    "success": False,
                    "message": "Invalid username or password.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "success": True,
                "message": "Login successful.",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


# Current user's profile
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=UserSerializer,
        tags=["Authentication"],
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)


# Admin creates a user.
# The serializer automatically assigns the Viewer role.
class CreateUserWithRoleView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request):
        serializer = CreateUserWithRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "success": True,
                "message": "User created successfully.",
                "data": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


# User CRUD: Admin only
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserWithRoleSerializer

        return UserSerializer


# Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=LogoutRequestSerializer,
        responses={
            205: MessageResponseSerializer,
            400: MessageResponseSerializer,
        },
        tags=["Authentication"],
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {
                    "success": False,
                    "message": "Refresh token is required.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "success": True,
                    "message": "Logout successful.",
                },
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception:
            return Response(
                {
                    "success": False,
                    "message": "Invalid refresh token.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


# Refresh access token
class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]
