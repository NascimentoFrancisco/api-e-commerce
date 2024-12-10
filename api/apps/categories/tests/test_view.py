# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=no-member
# pylint:disable=protected-access
import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from api.apps.categories.models import Categories
from api.apps.user.models import User
from api.apps.categories.serializers import CategoriesSerializer


class CategoriesViewTest(TestCase):

    def setUp(self):
        self.user = User(name="Teste", username="teste", email="teste@teste.com")
        self.user.is_superuser = True
        self.user.set_password("teste#123")
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client = APIClient()

        self.category = Categories(
            title="First Catrgory", description="For tests", status=True
        )
        self.category.save()

    def authenticate(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create(self):
        data = {"title": "Test", "description": "Testing", "status": False}
        self.authenticate()
        response = self.client.post("/api/v1/categories/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_category(self):
        self.authenticate()
        response = self.client.get(f"/api/v1/categories/{self.category.id}/")
        category = Categories.objects.get(pk=self.category.id)
        serializer = CategoriesSerializer(category)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_get_all_categroies(self):
        self.authenticate()
        response = self.client.get("/api/v1/categories/")
        categroies = Categories.objects.all()
        serializer = CategoriesSerializer(categroies, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)

    def test_update_category(self):
        data = {"title": "Test", "description": "Testing", "status": True}
        self.authenticate()
        response = self.client.put(
            f"/api/v1/categories/{self.category.id}/",
            json.dumps(data),
            content_type="application/json",
        )
        category = Categories.objects.get(pk=self.category.id)
        serializer = CategoriesSerializer(category)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), serializer.data)
