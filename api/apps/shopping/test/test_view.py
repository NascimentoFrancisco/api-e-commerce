# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=no-member
# pylint:disable=protected-access
import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from api.apps.user.models import User
from api.apps.categories.models import Categories
from api.apps.products.models import Product
from api.apps.shopping.models import Shopping

MY_GITHUB_PROFILE_PICTURE_URL = """
https://avatars.githubusercontent.com/u/86686689?s=400&u=4288eb5a6a3d09351a636891f9222a3db01ea5fa&v=4
"""


class ShoppingViewTest(TestCase):

    def setUp(self):
        self.user = User(name="Test", username="test", email="test@test.com")
        self.user.set_password("test#123")
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client = APIClient()

        self.category = Categories.objects.create(
            title="Teste", description="Teste de model"
        )
        self.category.save()

        self.product = Product(
            name="Test",
            user=self.user,
            description="Testing",
            category=self.category,
            amount=12,
            price=12.34,
            image_url=MY_GITHUB_PROFILE_PICTURE_URL,
        )
        self.product.save()

        self.product2 = Product(
            name="The Test",
            user=self.user,
            description="Testing",
            category=self.category,
            amount=12,
            price=12.34,
            image_url=MY_GITHUB_PROFILE_PICTURE_URL,
        )
        self.product2.save()

        self.shopping = Shopping(
            user=self.user, product=self.product, quantity_products=2
        )
        self.shopping.save()

    def authenticate(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create_insufficient_amount_products(self):
        self.authenticate()
        data = {
            "product_id": self.product2.id,
            "quantity_products": 18,
            "status": True,
            "payment_status": False,
        }
        response = self.client.post("/api/v1/shopping/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {"detail": "A quantidade solicitada excede o estoque disponível."},
        )

    def test_create(self):
        self.authenticate()
        data = {
            "product_id": self.product2.id,
            "quantity_products": 1,
            "status": True,
            "payment_status": False,
        }
        response = self.client.post("/api/v1/shopping/", data)
        self.product2.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.product2.amount, 11)

    def test_get_shopping(self):
        self.authenticate()
        response = self.client.get(f"/api/v1/shopping/{self.shopping.id}/")
        shopping_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(shopping_response["user"], str(self.shopping.user.id))
        self.assertEqual(
            shopping_response["product"]["id"], str(self.shopping.product.id)
        )
        self.assertEqual(
            shopping_response["quantity_products"], self.shopping.quantity_products
        )
        self.assertEqual(
            shopping_response["payment_status"], self.shopping.payment_status
        )

    def test_get_all_shoppings(self):
        self.authenticate()
        response = self.client.get("/api/v1/shopping/")
        shopping_response = response.json()
        shoppings = Shopping.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for index, shopping in enumerate(shoppings):
            self.assertEqual(shopping_response[index]["user"], str(shopping.user.id))
            self.assertEqual(
                shopping_response[index]["product"]["id"], str(shopping.product.id)
            )
            self.assertEqual(
                shopping_response[index]["quantity_products"],
                shopping.quantity_products,
            )
            self.assertEqual(
                shopping_response[index]["payment_status"], shopping.payment_status
            )

    def test_update_shopping(self):
        self.authenticate()
        data = {"status": False, "payment_status": True}
        response = self.client.patch(
            f"/api/v1/shopping/{self.shopping.id}/",
            json.dumps(data),
            content_type="application/json",
        )

        shopping_response = response.json()
        shopping = Shopping.objects.get(id=self.shopping.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(shopping_response["user"], str(shopping.user.id))
        self.assertEqual(shopping_response["product"]["id"], str(shopping.product.id))
        self.assertEqual(
            shopping_response["quantity_products"], shopping.quantity_products
        )
        self.assertEqual(shopping_response["payment_status"], shopping.payment_status)
        self.assertEqual(shopping_response["status"], shopping.status)

    def test_delete_shopping_not_permission(self):
        self.authenticate()
        response = self.client.delete(f"/api/v1/shopping/{self.shopping.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Shopping.objects.exists())

    def test_delete_shopping(self):
        self.user.is_superuser = True
        self.user.save()
        self.authenticate()
        response = self.client.delete(f"/api/v1/shopping/{self.shopping.id}/")
        self.product.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Shopping.objects.exists())
        self.assertEqual(self.product.amount, 14)
