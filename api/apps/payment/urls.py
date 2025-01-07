from django.urls import path, include
from rest_framework import routers
from api.apps.payment.views import PyamentView

app_name = "pyament"
router = routers.DefaultRouter()

router.register("", PyamentView, basename="pyament")

urlpatterns = [path("", include(router.urls))]
