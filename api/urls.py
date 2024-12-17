from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/user/", include("api.apps.user.urls"), name="user"),
    path("api/v1/categories/", include("api.apps.categories.urls"), name="categories"),
    path("api/v1/products/", include("api.apps.products.urls"), name="products"),
    path(
        "api/v1/shopping-cart/",
        include("api.apps.shopping_cart.urls"),
        name="shopping-cart",
    ),
    path("api/v1/shopping/", include("api.apps.shopping.urls"), name="shopping"),
]
