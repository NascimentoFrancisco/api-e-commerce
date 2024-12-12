# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=no-member
# pylint:disable=protected-access
from datetime import datetime
from django.test import TestCase
from api.apps.user.models import User
from api.apps.categories.models import Categories
from api.apps.products.models import Product

MY_GITHUB_PROFILE_PICTURE_URL = """
https://avatars.githubusercontent.com/u/86686689?s=400&u=4288eb5a6a3d09351a636891f9222a3db01ea5fa&v=4
"""


class ProductModelTest(TestCase):

    def setUp(self):
        self.user = User(name="Test", username="test", email="test@test.com")
        self.user.set_password("test#123")
        self.user.save()

        self.category = Categories.objects.create(
            title="Category test", description="Category to tests"
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

    def test_create(self):
        self.assertTrue(Product.objects.exists())

    def test_str(self):
        self.assertEqual(str(self.product), "Test")

    def test_description_value(self):
        self.assertEqual(self.product.description, "Testing")

    def test_slug_unique(self):
        attribute = Product._meta.get_field("slug")
        self.assertTrue(attribute.unique)

    def test_slug_value(self):
        self.assertEqual(self.product.slug, "test")

    def test_user_value(self):
        self.assertEqual(self.product.user, self.user)

    def test_category_value(self):
        self.assertEqual(self.product.category, self.category)

    def test_amount_value(self):
        self.assertEqual(self.product.amount, 12)

    def test_price_value(self):
        self.assertEqual(self.product.price, 12.34)

    def test_image_url_value(self):
        self.assertEqual(self.product.image_url, MY_GITHUB_PROFILE_PICTURE_URL)

    def test_created_at(self):
        self.assertIsInstance(self.product.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.product.updated_at, datetime)
