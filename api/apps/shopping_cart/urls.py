from django.urls import path, include
from rest_framework import routers
from api.apps.shopping_cart.views import ShoppingCartView

app_name = "shopping-cart"
router = routers.DefaultRouter()

router.register("", ShoppingCartView, basename="shopping-cart")

urlpatterns = [path("", include(router.urls))]
