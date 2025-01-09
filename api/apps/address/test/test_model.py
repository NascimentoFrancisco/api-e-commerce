# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=no-member
# pylint:disable=protected-access
from datetime import datetime
from django.test import TestCase
from api.apps.user.models import User
from api.apps.address.models import Address


class AddressModelTest(TestCase):

    def setUp(self):
        self.user = User(name="Test", username="test", email="test@test.com")
        self.user.set_password("test#123")
        self.user.save()

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

    def test_create(self):
        self.assertTrue(Address.objects.exists())

    def test_user_value(self):
        self.assertIsInstance(self.address.user, User)
        self.assertEqual(self.address.user.id, self.user.id)

    def test_address_values(self):
        self.assertEqual(self.address.cep, "65840000")
        self.assertEqual(self.address.city, "São Raimundo das Mangabeiras")
        self.assertEqual(self.address.state, "Maranhão")
        self.assertEqual(self.address.district, "Bairro")
        self.assertEqual(self.address.street, "Rua ruim")
        self.assertEqual(self.address.number, 22)
        self.assertEqual(self.address.complement, "Casa")
        self.assertEqual(self.address.phone_number, "99999999999")

    def test_created_at(self):
        self.assertIsInstance(self.address.created_at, datetime)

    def test_updated_at(self):
        self.assertIsInstance(self.address.updated_at, datetime)
