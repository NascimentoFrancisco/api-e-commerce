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
from api.apps.address.models import Address
from api.apps.payment.models import Payment, PaymentMethods

MY_GITHUB_PROFILE_PICTURE_URL = """
https://avatars.githubusercontent.com/u/86686689?s=400&u=4288eb5a6a3d09351a636891f9222a3db01ea5fa&v=4
"""


class PaymentViewTest(TestCase):
    def setUp(self):
        self.user = User(name="Test", username="test", email="test@test.com")
        self.user.set_password("test#123")
        self.user.save()

        self.user2 = User(name="Tests", username="tests", email="tests@test.com")
        self.user2.set_password("test#123")
        self.user2.save()

        refresh = RefreshToken.for_user(self.user2)
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
            price=50,
            image_url=MY_GITHUB_PROFILE_PICTURE_URL,
        )
        self.product.save()

        self.address = Address(
            user=self.user,
            cep="65840000",
            city="São Raimundo das Mangabeiras",
            state="Maranhão",
            district="Bairro",
            street="Rua ruim",
            number=22,
            complement="Casa",
            phone_number="99999999999",
        )
        self.address.save()

        self.shopping = Shopping(
            user=self.user,
            product=self.product,
            quantity_products=2,
            value=self.product.price * 2,
            shipping_value=3.4,
            address=self.address,
        )
        self.shopping.save()

        self.payment = Payment(
            user=self.user,
            shopping=self.shopping,
            payment_method=PaymentMethods.CREDIT_CARD,
            divided_into=1,
            value=50,
            total_value=50,
        )
        self.payment.save()

    def authenticate(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create(self):
        self.authenticate()
        data = {
            "shopping": self.shopping.id,
            "payment_method": "CTC",
            "divided_into": 2,
            "value": 26.50,
            "total_value": 53,
        }
        response = self.client.post("/api/v1/payment/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_payment(self):
        self.authenticate()
        response = self.client.get(f"/api/v1/payment/{self.payment.id}/")
        payment_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payment_response["user"], str(self.payment.user.id))
        self.assertEqual(payment_response["shopping"], str(self.payment.shopping.id))
        self.assertEqual(payment_response["divided_into"], self.payment.divided_into)
        self.assertEqual(
            payment_response["payment_method"], self.payment.payment_method
        )
        self.assertEqual(float(payment_response["value"]), self.payment.value)
        self.assertEqual(
            float(payment_response["total_value"]), self.payment.total_value
        )

    def test_all_payments(self):
        self.authenticate()
        response = self.client.get("/api/v1/payment/")
        payment_response = response.json()
        payments = Payment.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for index, payment in enumerate(payments):
            self.assertEqual(payment_response[index]["user"], str(payment.user.id))
            self.assertEqual(
                payment_response[index]["shopping"], str(payment.shopping.id)
            )
            self.assertEqual(
                payment_response[index]["divided_into"], payment.divided_into
            )
            self.assertEqual(
                payment_response[index]["payment_method"], payment.payment_method
            )
            self.assertEqual(
                float(payment_response[index]["value"]), float(payment.value)
            )
            self.assertEqual(
                float(payment_response[index]["total_value"]),
                float(payment.total_value),
            )

    def test_update_payment(self):
        self.authenticate()
        data = {"payment_method": "PIX", "divided_into": 1}
        response = self.client.patch(
            f"/api/v1/payment/{self.payment.id}/",
            json.dumps(data),
            content_type="application/json",
        )
        payment = Payment.objects.get(id=self.payment.id)
        payment_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payment_response["user"], str(payment.user.id))
        self.assertEqual(payment_response["shopping"], str(payment.shopping.id))
        self.assertEqual(payment_response["divided_into"], payment.divided_into)
        self.assertEqual(payment_response["payment_method"], payment.payment_method)
        self.assertEqual(float(payment_response["value"]), payment.value)
        self.assertEqual(float(payment_response["total_value"]), payment.total_value)

    def test_delete_payment(self):
        self.authenticate()
        shopping_id = self.payment.shopping.id
        response = self.client.delete(f"/api/v1/payment/{self.payment.id}/")
        shopping = Shopping.objects.get(id=shopping_id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(shopping.payment_status)
