import json
from django.test import TestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from api.apps.user.models import User
from api.apps.user.serizalizers import UpdateUserSerializer, UserSerializer


class UserViewsTest(TestCase):

    def setUp(self):
        self.user = User(name="Teste", username="teste", email="teste@teste.com")
        self.user.set_password("teste#123")
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client = APIClient()

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_user_correct(self):
        data = {
            "name": "TesteCase",
            "username": "testeCase",
            "email": "testecase@teste.com",
            "password1": "test#123",
            "password2": "test#123",
        }
        response = self.client.post("/api/v1/user/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user__different_passwords(self):
        data = {
            "name": "TesteCase",
            "username": "testeCase",
            "email": "testecase@teste.com",
            "password1": "test#123",
            "password2": "test#1238",
        }
        response = self.client.post("/api/v1/user/", data)
        response_dict = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_dict["password1"][0], "Senhas diferentes")

    def test_update_user(self):
        data = {
            "name": "TestTesCase",
            "username": "testesCase",
            "email": "testescase@teste.com",
        }
        self.authenticate()
        response = self.client.put(
            f"/api/v1/user/{self.user.id}/",
            json.dumps(data),
            content_type="application/json",
        )
        user = User.objects.get(pk=self.user.id)
        serializer = UpdateUserSerializer(user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_get_user(self):
        self.authenticate()
        respose = self.client.get(f"/api/v1/user/{self.user.id}/")
        user = User.objects.get(pk=self.user.id)
        serializer = UserSerializer(user)

        self.assertEqual(respose.status_code, status.HTTP_200_OK)
        self.assertEqual(respose.json(), serializer.data)

    def test_get_all_users(self):
        self.authenticate()
        response = self.client.get("/api/v1/user/")
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
