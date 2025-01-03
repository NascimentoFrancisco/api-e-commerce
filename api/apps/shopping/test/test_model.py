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

MY_GITHUB_PROFILE_PICTURE_URL = """
https://avatars.githubusercontent.com/u/86686689?s=400&u=4288eb5a6a3d09351a636891f9222a3db01ea5fa&v=4
"""


class ShoppingModelTest(TestCase):

    def setUp(self):
        self.user = User(name="Test", username="test", email="test@test.com")
        self.user.set_password("test#123")
        self.user.save()

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

        self.shopping = Shopping(
            user=self.user, product=self.product, quantity_products=2
        )
        self.shopping.save()

    def test_create(self):
        self.assertTrue(Shopping.objects.exists())

    def test_str(self):
        self.assertEqual(str(self.shopping), "Test")

    def test_product_value(self):
        self.assertIsInstance(self.shopping.product, Product)

    def test_user_value(self):
        self.assertIsInstance(self.product.user, User)

    def test_status_shopping_cart(self):
        self.assertTrue(self.shopping.status)

    def test_slug_value(self):
        self.assertEqual(self.shopping.slug, "test-test")

    def test_default_value_status(self):
        self.assertTrue(self.shopping.status)

    def test_defaulft_value_cancelled(self):
        self.assertFalse(self.shopping.cancelled)

    def test_default_payment_status(self):
        self.assertFalse(self.shopping.payment_status)

    def test_created_at(self):
        self.assertIsInstance(self.product.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.product.updated_at, datetime)
