
from rest_framework import viewsets
from .models import Category
from .category_serializer import CategorySerializer
from .filters import filter_categories
from .permissions import AdminOrReadOnly



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [
        AdminOrReadOnly
    ]
    def get_queryset(self):
        queryset = super().get_queryset()

        return filter_categories(
            queryset,
            self.request.query_params
        )

    