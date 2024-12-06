"""Module containing user management settings."""

from typing import Any
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User


class UserManager(BaseUserManager):
    """Class to manage internal user characteristics and super users when they are created"""

    use_in_migrations = True

    def __create_user(self, username: str, password: str, **extra_fields: Any) -> User:
        user: User = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, password: str, **extra_fields: Any) -> User:
        """Public method of the class to create conventional user
        * parameters:
                - username: String to generate a unique username,
                - password: String to generate a password,
                - **extra_fields: Other information regarding the User base model
            * retrun:
                - An object of type User, from 'django.contrib.auth.models'
        """
        return self.__create_user(username, password, **extra_fields)

    def create_superuser(
        self, username: str, password: str, **extra_fields: Any
    ) -> User:
        """Public method of the class to create super user with some extra permissions.
        * parameters:
                - username: String to generate a unique username,
                - password: String to generate a password,
                - **extra_fields: Other information regarding the User base model
            * retrun:
                - An object of type User, from 'django.contrib.auth.models'
        """
        user: User = self.__create_user(username, password, **extra_fields)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
