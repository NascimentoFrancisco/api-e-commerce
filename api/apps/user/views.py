from rest_framework.viewsets import ModelViewSet
from api.apps.user.models import User
from api.apps.user.serizalizers import UserSerializer, UpdateUserSerializer


class UserViewSet(ModelViewSet):
    """Views inherent to the User model"""

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "update":
            return UpdateUserSerializer
        return UserSerializer
