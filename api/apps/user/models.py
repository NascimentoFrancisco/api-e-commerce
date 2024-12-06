import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from api.managers.user_maneger import UserManager


class User(AbstractUser, PermissionsMixin):
    """User and super user model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    name = models.CharField("Nome", max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "username"

    def __str__(self) -> str:
        return f"{self.username}"

    class Meta:
        """Meta Class"""

        verbose_name = "usuário"
        verbose_name_plural = "usuários"
