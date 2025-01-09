# pylint: disable=unused-argument
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-class-docstring
# pylint: disable= unused-import
from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api.apps.payment"

    def ready(self):
        import api.apps.payment.signals.signals
