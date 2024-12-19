# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=no-member
# pylint:disable=protected-access
from typing import Dict
from django.test import TestCase
from rest_framework import status
from api.apps.user.models import User


class AuthenticationJwtTest(TestCase):
    def setUp(self):
        self.user = User(name="Teste", username="teste", email="teste@teste.com")
        self.user.set_password("teste#123")
        self.user.save()

        data = {"username": "teste", "password": "teste#123"}

        response = self.client.post("/api/v1/token/", data)
        self.response_auth: Dict = response.json()

    def test_get_token_ok(self):
        data = {"username": "teste", "password": "teste#123"}

        response = self.client.post("/api/v1/token/", data)
        response_dict: Dict = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response_dict.keys())
        self.assertTrue("refresh" in response_dict.keys())

    def test_get_token_wrong(self):
        data = {"username": "teste", "password": "teste#1235"}

        response = self.client.post("/api/v1/token/", data)
        response_dict: Dict = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response_dict["detail"],
            "No active account found with the given credentials",
        )
        self.assertFalse("access" in response_dict.keys())
        self.assertFalse("refresh" in response_dict.keys())

    def test_refresh_token_ok(self):

        response_refresh = self.client.post(
            "/api/v1/token/refresh/", {"refresh": self.response_auth["refresh"]}
        )
        response_refresh_dict: Dict = response_refresh.json()

        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response_refresh_dict.keys())

    def test_refresh_token_wrong(self):

        response_refresh = self.client.post(
            "/api/v1/token/refresh/", {"refresh": "token_wrong"}
        )
        response_refresh_dict: Dict = response_refresh.json()

        self.assertEqual(response_refresh.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse("access" in response_refresh_dict.keys())
