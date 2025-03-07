# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=no-member
# pylint:disable=protected-access
from datetime import datetime
from django.test import TestCase
from api.apps.user.models import User
from api.apps.categories.models import Categories
from api.apps.products.models import Product
from api.apps.shopping.models import Shopping
from api.apps.address.models import Address
from api.apps.payment.models import Payment, PaymentMethods

MY_GITHUB_PROFILE_PICTURE_URL = """
https://avatars.githubusercontent.com/u/86686689?s=400&u=4288eb5a6a3d09351a636891f9222a3db01ea5fa&v=4
"""


class PyamentModelTest(TestCase):

    def setUp(self):
        self.user = User(name="Test", username="test", email="test@test.com")
        self.user.set_password("test#123")
        self.user.save()

        self.user2 = User(name="Tests", username="tests", email="tests@test.com")
        self.user2.set_password("test#123")
        self.user2.save()

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
            user=self.user2,
            shopping=self.shopping,
            payment_method=PaymentMethods.CREDIT_CARD,
            divided_into=1,
            value=12.34,
            total_value=12.34,
        )
        self.payment.save()

    def test_create(self):
        self.assertTrue(Payment.objects.exists())

    def test_update_payment_status_after_create(self):
        shopping = Shopping.objects.get(pk=self.payment.shopping.id)
        self.assertTrue(shopping.payment_status, True)

    def test_value_by_payment(self):
        self.assertEqual(self.payment.value, 12.34)

    def test_payment_method(self):
        self.assertEqual(self.payment.payment_method, "CTC")

    def test_payment_divided_into(self):
        self.assertEqual(self.payment.divided_into, 1)

    def test_created_at(self):
        self.assertIsInstance(self.payment.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.payment.updated_at, datetime)

    def test_update_payment_status_after_delete(self):
        shopping_id = self.payment.shopping.id
        self.payment.delete()
        shopping = Shopping.objects.get(pk=shopping_id)

        self.assertFalse(shopping.payment_status)
