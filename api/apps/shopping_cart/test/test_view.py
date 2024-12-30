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
from api.apps.shopping_cart.models import ShoppingCart

MY_GITHUB_PROFILE_PICTURE_URL = """
https://avatars.githubusercontent.com/u/86686689?s=400&u=4288eb5a6a3d09351a636891f9222a3db01ea5fa&v=4
"""


class ShoppingCartViewTest(TestCase):

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
            name="Tests",
            user=self.user,
            description="Testings",
            category=self.category,
            amount=12,
            price=12.34,
            image_url=MY_GITHUB_PROFILE_PICTURE_URL,
        )
        self.product2.save()

        self.shopping_cart = ShoppingCart(user=self.user, product=self.product)
        self.shopping_cart.save()

    def authenticate(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create(self):
        self.authenticate()
        data = {"product_id": self.product2.id, "status": True}
        response = self.client.post("/api/v1/shopping-cart/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_shopping_cart_existing_product(self):
        self.authenticate()
        data = {"product_id": self.product.id, "status": True}
        response = self.client.post("/api/v1/shopping-cart/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["detail"],
            "O produto já está no carrinho para este usuário.",
        )

    def test_get_shopping_cart(self):
        self.authenticate()
        response = self.client.get(f"/api/v1/shopping-cart/{self.shopping_cart.id}/")
        shopping_cart_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            shopping_cart_response["user"], str(self.shopping_cart.user.id)
        )
        self.assertEqual(
            shopping_cart_response["product"]["id"], str(self.shopping_cart.product.id)
        )
        self.assertEqual(shopping_cart_response["status"], self.shopping_cart.status)

    def test_get_all_shopping_cart(self):
        self.authenticate()
        response = self.client.get("/api/v1/shopping-cart/")
        shopping_carts = ShoppingCart.objects.all()
        shopping_cart_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for index, shopping_cart in enumerate(shopping_carts):
            self.assertEqual(
                shopping_cart_response[index]["user"], str(shopping_cart.user.id)
            )
            self.assertEqual(
                shopping_cart_response[index]["product"]["id"],
                str(shopping_cart.product.id),
            )
            self.assertEqual(
                shopping_cart_response[index]["status"], shopping_cart.status
            )

    def test_update_hopping_cart(self):
        self.authenticate()
        data = {"status": False}
        response = self.client.patch(
            f"/api/v1/shopping-cart/{self.shopping_cart.id}/",
            json.dumps(data),
            content_type="application/json",
        )

        shopping_cart_response = response.json()
        shopping_cart = ShoppingCart.objects.get(id=self.shopping_cart.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(shopping_cart_response["user"], str(shopping_cart.user.id))
        self.assertEqual(
            shopping_cart_response["product"]["id"], str(shopping_cart.product.id)
        )
        self.assertEqual(shopping_cart_response["status"], shopping_cart.status)

    def test_delete_hopping_cart(self):
        self.authenticate()
        response = self.client.delete(f"/api/v1/shopping-cart/{self.shopping_cart.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ShoppingCart.objects.exists())
