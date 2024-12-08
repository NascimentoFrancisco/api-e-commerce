from datetime import datetime
from django.test import TestCase
from api.apps.categories.models import Categories


class CategoriesModelTest(TestCase):

    def setUp(self) -> None:
        self.category = Categories.objects.create(
            title="Teste", description="Teste de model"
        )
        self.category.save()

    def test_create(self):
        self.assertTrue(Categories.objects.exists())

    def test_str(self):
        self.assertEqual(str(self.category), "Teste")

    def test_title_can_not_null_blank(self):
        attribute = Categories._meta.get_field("title")
        self.assertFalse(attribute.blank)
        self.assertFalse(attribute.null)

    def test_description_can_not_null_blank(self):
        attribute = Categories._meta.get_field("description")
        self.assertFalse(attribute.blank)
        self.assertFalse(attribute.null)

    def test_default_value_status_true(self):
        self.assertTrue(self.category.status)

    def test_value_title(self):
        self.assertEqual(self.category.title, "Teste")

    def test_value_description(self):
        self.assertEqual(self.category.description, "Teste de model")

    def test_created_at(self):
        self.assertIsInstance(self.category.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.category.updated_at, datetime)
