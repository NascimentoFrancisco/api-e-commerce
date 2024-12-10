# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=no-member
# pylint:disable=protected-access
from datetime import datetime
from django.test import TestCase
from api.apps.user.models import User


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User(name="Teste", username="teste", email="teste@teste.com")
        self.user.set_password("teste#123")
        self.user.save()

    def test_create(self):
        self.assertTrue(User.objects.exists())

    def test_str(self):
        self.assertEqual(str(self.user), "teste")

    def test_username_value(self):
        self.assertEqual(self.user.username, "teste")

    def test_username_unique(self):
        attribute = User._meta.get_field("username")
        self.assertTrue(attribute.unique)

    def test_name_value(self):
        self.assertEqual(self.user.name, "Teste")

    def test_email_value(self):
        self.assertEqual(self.user.email, "teste@teste.com")

    def test_email_unique(self):
        attribute = User._meta.get_field("email")
        self.assertTrue(attribute.unique)

    def test_password_correct(self):
        self.assertTrue(self.user.check_password("teste#123"))

    def test_password_wrong(self):
        self.assertFalse(self.user.check_password("fsafsaf"))

    def test_user_active_default(self):
        self.assertTrue(self.user.is_active)

    def teste_user_is_superuser_default(self):
        self.assertFalse(self.user.is_superuser)

    def test_created_at(self):
        self.assertIsInstance(self.user.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.user.updated_at, datetime)
