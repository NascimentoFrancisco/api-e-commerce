# pylint:disable=missing-function-docstring
# pylint:disable=missing-class-docstring
# pylint:disable=no-member
# pylint:disable=protected-access
from io import BytesIO
from django.test import TestCase
from django.conf import settings
from api.services.firebase.storage import HandleFirebaseStorage


class TestHandleFirebaseStorage(TestCase):
    def setUp(self):
        self.storage_handler = HandleFirebaseStorage()
        self.test_file = BytesIO(b"test data for integration")
        self.updated_file = BytesIO(b"updated image content")
        self.test_image_name = "test_image_integration"
        self.test_content_type = "image/jpeg"

    def test_upload_image_to_storage(self):
        public_url = self.storage_handler.upload_image_to_storage(
            self.test_file, self.test_image_name, self.test_content_type
        )

        self.assertTrue(public_url.startswith("https"), "O URL retornado não é válido.")
        self.assertIn(
            self.test_image_name,
            public_url,
            "O nome do arquivo não está no URL retornado.",
        )

    def test_update_image_in_storage(self):
        updated_url = self.storage_handler.update_image_in_storage(
            self.updated_file, self.test_image_name, self.test_content_type
        )

        self.assertTrue(updated_url.startswith("http"), "O URL retornado não é válido.")
        self.assertIn(
            self.test_image_name,
            updated_url,
            "O nome do arquivo não está no URL retornado.",
        )

        blob = self.storage_handler.bucket.blob(
            f"{settings.FIREBASE_PATH}{self.test_image_name}"
        )
        downloaded_data = blob.download_as_bytes()
        self.assertEqual(
            downloaded_data,
            b"updated image content",
            "O conteúdo do arquivo não foi atualizado corretamente.",
        )

    def tearDown(self):
        """Remove the test file from Firebase Storage"""
        blob = self.storage_handler.bucket.blob(
            f"{settings.FIREBASE_PATH}{self.test_image_name}"
        )
        blob.delete()
