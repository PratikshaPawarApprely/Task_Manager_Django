from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from .pagination import CustomPagination


class BaseListCreateView(ListCreateAPIView):
    """
    Common GET list + POST create API
    """
    pagination_class = CustomPagination


class BaseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Common GET single + PUT + PATCH + DELETE API
    """
    pass
