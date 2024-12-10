from django.urls import path, include
from rest_framework import routers
from api.apps.categories.views import CategoriesView

app_name = "categories"
router = routers.DefaultRouter()

router.register("", CategoriesView, basename="categories")

urlpatterns = [path("", include(router.urls))]
