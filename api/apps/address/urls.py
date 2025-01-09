from django.urls import path, include
from rest_framework import routers
from api.apps.address.views import AddressView

app_name = "address"
router = routers.DefaultRouter()

router.register("", AddressView, basename="shopping")

urlpatterns = [path("", include(router.urls))]
