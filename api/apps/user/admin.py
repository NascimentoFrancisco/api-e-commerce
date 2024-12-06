from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.apps.user.models import User


class UserAdminConfig(UserAdmin):
    """User Configuration Class in Admin Panel"""

    model = User
    list_display = (
        "username",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "username",
        "email",
        "is_superuser",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "name", "email", "password")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "name",
                    "password1",
                    "password2",
                    "is_superuser",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(User, UserAdminConfig)
