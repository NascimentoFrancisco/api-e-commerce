# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=no-member
# pylint:disable=protected-access
from io import BytesIO
from unittest.mock import patch
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from api.apps.products.models import Product
from api.apps.categories.models import Categories
from api.apps.user.models import User


class ProductViewTest(TestCase):

    def setUp(self):
        self.user = User(name="Teste", username="teste", email="teste@teste.com")
        self.user.set_password("teste#123")
        self.user.is_superuser = True
        self.user.save()

        self.category = Categories(
            title="First Catrgory", description="For tests", status=True
        )
        self.category.save()

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client = APIClient()

        self.product = Product(
            name="Test Product",
            user=self.user,
            description="Test Description",
            category=self.category,
            amount=10,
            price=99.99,
            slug="test-product",
            status=True,
            image_url="https://example.com/test-image.jpg",
        )
        self.product.save()

    def authenticate(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    @patch(
        "api.services.firebase.storage.HandleFirebaseStorage.upload_image_to_storage"
    )
    def test_create_product(self, mock_upload):
        mock_upload.return_value = "https://example.com/test-uploaded-image.jpg"

        image_data = BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(image_data, format="JPEG")
        image_data.seek(0)
        uploaded_image = SimpleUploadedFile(
            name="test_image.jpg", content=image_data.read(), content_type="image/jpeg"
        )

        data = {
            "name": "New Product",
            "description": "New Description",
            "category": self.category.id,
            "amount": 5,
            "price": 49.99,
            "status": True,
            "image": uploaded_image,
        }

        self.authenticate()
        response = self.client.post("/api/v1/products/", data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

        mock_upload.assert_called_once()

        created_product = Product.objects.last()
        self.assertEqual(
            created_product.image_url, "https://example.com/test-uploaded-image.jpg"
        )

    def test_get_product(self):
        response = self.client.get(f"/api/v1/products/{self.product.id}/")
        product = Product.objects.get(pk=self.product.id)
        product_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(product_response["name"], product.name)
        self.assertEqual(product_response["user"]["id"], str(product.user.id))
        self.assertEqual(product_response["description"], product.description)
        self.assertEqual(product_response["category"], str(product.category.id))
        self.assertEqual(product_response["amount"], product.amount)
        self.assertEqual(float(product_response["price"]), float(product.price))
        self.assertEqual(product_response["status"], product.status)
        self.assertEqual(product_response["image_url"], product.image_url)

    def test_get_all_products(self):
        response = self.client.get("/api/v1/products/")
        products = Product.objects.all()
        product_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for index, product in enumerate(products):
            self.assertEqual(product_response[index]["name"], product.name)
            self.assertEqual(
                product_response[index]["user"]["id"], str(product.user.id)
            )
            self.assertEqual(
                product_response[index]["description"], product.description
            )
            self.assertEqual(
                product_response[index]["category"], str(product.category.id)
            )
            self.assertEqual(product_response[index]["amount"], product.amount)
            self.assertEqual(
                float(product_response[index]["price"]), float(product.price)
            )
            self.assertEqual(product_response[index]["status"], product.status)
            self.assertEqual(product_response[index]["image_url"], product.image_url)

    def test_get_all_products_by_authenticated_user(self):
        self.authenticate()
        response = self.client.get("/api/v1/products/")
        products = Product.objects.all()
        product_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for index, product in enumerate(products):
            self.assertEqual(product_response[index]["name"], product.name)
            self.assertEqual(
                product_response[index]["user"]["id"], str(product.user.id)
            )
            self.assertEqual(
                product_response[index]["description"], product.description
            )
            self.assertEqual(
                product_response[index]["category"], str(product.category.id)
            )
            self.assertEqual(product_response[index]["amount"], product.amount)
            self.assertEqual(
                float(product_response[index]["price"]), float(product.price)
            )
            self.assertEqual(product_response[index]["status"], product.status)
            self.assertEqual(product_response[index]["image_url"], product.image_url)

    @patch(
        "api.services.firebase.storage.HandleFirebaseStorage.update_image_in_storage"
    )
    @patch("api.services.firebase.storage.HandleFirebaseStorage.delete_blob")
    def test_update_product(self, mock_delete_blob, mock_update_image):
        mock_update_image.return_value = "https://example.com/new-uploaded-image.jpg"

        new_image_data = BytesIO()
        new_image = Image.new("RGB", (100, 100), color="blue")
        new_image.save(new_image_data, format="JPEG")
        new_image_data.seek(0)
        new_uploaded_image = SimpleUploadedFile(
            name="new_test_image.jpg",
            content=new_image_data.read(),
            content_type="image/jpeg",
        )

        updated_data = {
            "name": "Updated Product",
            "description": "Updated Description",
            "category": self.category.id,
            "amount": 15,
            "price": 79.99,
            "status": False,
            "image": new_uploaded_image,
        }

        self.authenticate()
        response = self.client.put(
            f"/api/v1/products/{self.product.id}/", updated_data, format="multipart"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")
        self.assertEqual(self.product.description, "Updated Description")
        self.assertEqual(self.product.amount, 15)
        self.assertEqual(float(self.product.price), 79.99)
        self.assertFalse(self.product.status)
        self.assertEqual(
            self.product.image_url, "https://example.com/new-uploaded-image.jpg"
        )

        mock_delete_blob.assert_called_once()
        mock_update_image.assert_called_once()
