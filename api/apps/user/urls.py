from django.urls import path, include
from rest_framework import routers
from api.apps.user.views import UserViewSet

app_name = "user"
router = routers.DefaultRouter()

router.register("", UserViewSet, basename="user")

urlpatterns = [path("", include(router.urls))]
