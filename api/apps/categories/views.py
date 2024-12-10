# pylint: disable=no-member
from rest_framework.viewsets import ModelViewSet
from api.apps.categories.models import Categories
from api.apps.categories.serializers import CategoriesSerializer
from api.apps.categories.permissions import IsSuperUserOrReadOnly


class CategoriesView(ModelViewSet):
    """View class for the Categories model"""

    permission_classes = [IsSuperUserOrReadOnly]
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
