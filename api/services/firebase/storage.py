from io import BytesIO
import firebase_admin
from django.conf import settings
from firebase_admin import credentials, storage

credential = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(
    credential, {"storageBucket": settings.FIREBASE_STORAGE_BUCKET}
)


class HandleFirebaseStorage:
    """Class that manages operations related to Firebase Storage"""

    def __init__(self) -> None:
        self.bucket = storage.bucket()
        self.firebase_path = settings.FIREBASE_PATH

    def upload_image_to_storage(
        self, local_file_path: BytesIO, image_name: str, content_type: str
    ) -> str:
        """Method responsible for sending an image to the Firebase storage
        - parameters:
            * local_file_path: File sent in BytesIO format
            * image_name: Name chosen for image, being a str
            * content_type: content type to save the image of the same type without distortions
        - return:
            * public_url: A str containing the public URL of the image saved in the storage
        """
        firebase_path = self.firebase_path + image_name
        blob = self.bucket.blob(firebase_path)
        blob.upload_from_file(local_file_path, content_type=content_type)
        blob.make_public()

        return blob.public_url

    def update_image_in_storage(
        self, local_file_path: BytesIO, image_name: str, content_type: str
    ) -> str:
        """Method to replace an existing image in the Firebase storage
        - parameters:
            * local_file_path: File sent in BytesIO format
            * image_name: Name of the image to be replaced
            * content_type: Content type of the new image
        - return:
            * public_url: A string containing the public URL of the updated image
        """
        firebase_path = self.firebase_path + image_name
        blob = self.bucket.blob(firebase_path)

        if blob.exists():
            blob.delete()

        blob.upload_from_file(local_file_path, content_type=content_type)
        blob.make_public()

        return blob.public_url
