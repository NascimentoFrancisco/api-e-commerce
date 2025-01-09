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
from api.apps.address.models import Address


class AddressViewTest(TestCase):

    def setUp(self):
        self.user = User(name="Test", username="test", email="test@test.com")
        self.user.set_password("test#123")
        self.user.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client = APIClient()

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

    def authenticate(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_create(self):
        data = {
            "user": self.user,
            "cep": "65840000",
            "city": "São Raimundo das Mangabeiras",
            "state": "Maranhão",
            "district": "Bairro",
            "street": "Rua ruim",
            "number": 22,
            "complement": "Casa",
            "phone_number": "99999999999",
        }
        self.authenticate()
        response = self.client.post("/api/v1/address/", data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.count(), 2)

    def test_get_address(self):
        self.authenticate()
        response = self.client.get(f"/api/v1/address/{self.address.id}/")
        address_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(address_response["user"]["id"], str(self.user.id))
        self.assertEqual(address_response["cep"], self.address.cep)
        self.assertEqual(address_response["city"], self.address.city)
        self.assertEqual(address_response["state"], self.address.state)
        self.assertEqual(address_response["district"], self.address.district)
        self.assertEqual(address_response["street"], self.address.street)
        self.assertEqual(address_response["number"], self.address.number)
        self.assertEqual(address_response["complement"], self.address.complement)
        self.assertEqual(address_response["phone_number"], self.address.phone_number)

    def test_get_all_address(self):
        self.authenticate()
        response = self.client.get("/api/v1/address/")
        address_response = response.json()
        addresses = Address.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for index, address in enumerate(addresses):
            self.assertEqual(
                address_response[index]["user"]["id"], str(address.user.id)
            )
            self.assertEqual(address_response[index]["cep"], address.cep)
            self.assertEqual(address_response[index]["city"], address.city)
            self.assertEqual(address_response[index]["state"], address.state)
            self.assertEqual(address_response[index]["district"], address.district)
            self.assertEqual(address_response[index]["street"], address.street)
            self.assertEqual(address_response[index]["number"], address.number)
            self.assertEqual(address_response[index]["complement"], address.complement)
            self.assertEqual(
                address_response[index]["phone_number"], address.phone_number
            )

    def test_update_address(self):
        data = {
            "cep": "65845000",
            "number": 222,
            "complement": "Casa nova",
            "phone_number": "99999998888",
        }
        self.authenticate()
        response = self.client.patch(
            f"/api/v1/address/{self.address.id}/",
            json.dumps(data),
            content_type="application/json",
        )
        address_response = response.json()
        address = Address.objects.get(id=self.address.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(address_response["cep"], address.cep)
        self.assertEqual(address_response["number"], address.number)
        self.assertEqual(address_response["complement"], address.complement)
        self.assertEqual(address_response["phone_number"], address.phone_number)

    def test_delete_address(self):
        self.authenticate()
        response = self.client.delete(f"/api/v1/address/{self.address.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Address.objects.count(), 0)
