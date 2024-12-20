from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from api.apps.user.models import User
from api.apps.user.serializers import (
    UserSerializer,
    UpdateUserSerializer,
    ChangePasswordSerializer,
)
from api.apps.user.permissions import IsAuthenticatedOrJustPostMethod


class UserViewSet(ModelViewSet):
    """Views inherent to the User model"""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrJustPostMethod]

    def get_serializer_class(self):
        if "change-password" in self.request.path:
            return ChangePasswordSerializer
        if self.action == "update":
            return UpdateUserSerializer
        return UserSerializer

    @swagger_auto_schema(
        method="put",
        request_body=ChangePasswordSerializer,
    )
    @action(detail=False, methods=["put"], url_path="change-password")
    def change_password(self, request):
        """Endpoint to change the password of the logged-in user"""

        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = request.user
        serializer.update(user, serializer.validated_data)

        return Response(
            {"detail": "Senha alterada com sucesso!"}, status=status.HTTP_200_OK
        )
