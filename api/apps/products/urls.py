from django.urls import path, include
from rest_framework import routers
from api.apps.products.views import ProductView

app_name = "products"
router = routers.DefaultRouter()

router.register("", ProductView, basename="products")

urlpatterns = [path("", include(router.urls))]
