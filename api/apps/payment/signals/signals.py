# pylint: disable=unused-argument
from typing import Type
from django.db.models import Model
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from api.apps.payment.models import Payment


@receiver(post_save, sender=Payment)
def update_payment_status_shopping(
    sender: Type[Model], instance: Payment, created: bool, **kwargs
) -> None:
    """
    Signal to update the `payment_status` attribute of the related Shopping instance
    whenever a new Payment instance is created.
    """
    if created:
        shopping = instance.shopping
        shopping.payment_status = True
        shopping.save()


@receiver(post_delete, sender=Payment)
def reset_payment_status_shopping(
    sender: Type[Model], instance: Payment, **kwargs
) -> None:
    """
    Signal to update the `payment_status` attribute of the related Shopping instance
    to False when a Payment instance is deleted.
    """
    shopping = instance.shopping
    shopping.payment_status = False
    shopping.save()
