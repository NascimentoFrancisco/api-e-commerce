from django.urls import path, include
from rest_framework import routers
from api.apps.shopping.views import ShoppingView

app_name = "shopping"
router = routers.DefaultRouter()

router.register("", ShoppingView, basename="shopping")

urlpatterns = [path("", include(router.urls))]
