from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from api.auth.custom_token_obtain.view import CustomTokenObtainPairView


schema_view = get_schema_view(
    openapi.Info(
        title="Api E-commerce.",
        default_version="v1",
        description="Api genérica de um E-commerce.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="francisco.ads.dev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(
        "api/v1/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
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
