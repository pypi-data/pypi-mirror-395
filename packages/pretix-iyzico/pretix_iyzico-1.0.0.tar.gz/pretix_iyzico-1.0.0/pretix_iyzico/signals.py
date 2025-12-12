from django.dispatch import receiver
from pretix.base.signals import register_payment_providers

from .payment import IyzicoProvider


@receiver(register_payment_providers, dispatch_uid="payment_iyzico")
def register_payment_provider(sender, **kwargs):
    return IyzicoProvider
