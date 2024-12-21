from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from api.auth.custom_token_obtain.serializer import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to use the CustomTokenObtainPairSerializer to be
    able to return the logged in user id along with the tokens
    """

    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Obtenha o token de acesso e o ID do usuário autenticado.",
        responses={
            200: openapi.Response(
                description="Token gerado com sucesso.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "refresh": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Token de refresh."
                        ),
                        "access": openapi.Schema(
                            type=openapi.TYPE_STRING, description="Token de acesso."
                        ),
                        "user_id": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="ID do usuário autenticado.",
                        ),
                    },
                ),
            ),
            400: openapi.Response(
                description="Erro de validação.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "detail": openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description="Mensagem detalhada do erro.",
                        )
                    },
                ),
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """Overrides the POST description in the documentation"""
        return super().post(request, *args, **kwargs)
