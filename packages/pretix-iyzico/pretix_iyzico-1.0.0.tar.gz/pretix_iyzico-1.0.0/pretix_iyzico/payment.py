import base64
import hashlib
import json
import logging
import requests
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.payment import BasePaymentProvider, PaymentException

logger = logging.getLogger(__name__)


class IyzicoProvider(BasePaymentProvider):
    identifier = "iyzico"
    verbose_name = _("iyzico")
    execute_payment_needs_user = True

    def checkout_confirm_render(self, request, order=None, info_data=None):
        """Render payment confirmation details on checkout page"""
        return _(
            "After you submit your order, you will be redirected to iyzico "
            "to complete your payment securely."
        )

    def execute_payment(self, request, payment):
        """Execute the payment by redirecting to iyzico payment page"""
        try:
            payment_url = self._initialize_payment(request, payment.order, payment)
            if payment_url:
                return payment_url
            else:
                raise PaymentException(
                    _("Payment initialization failed. Please try again.")
                )
        except Exception as e:
            logger.error(f"iyzico payment execution error: {str(e)}")
            raise PaymentException(_("Payment error occurred. Please try again."))

    @property
    def settings_form_fields(self):
        from django import forms

        fields = {
            "_enabled": forms.BooleanField(
                label=_("Enable payment method"),
                required=False,
            ),
            "api_key": forms.CharField(
                label=_("API Key"),
                required=False,
                help_text=_("iyzico API Key"),
            ),
            "secret_key": forms.CharField(
                label=_("Secret Key"),
                required=False,
                widget=forms.PasswordInput(render_value=True),
                help_text=_("iyzico Secret Key"),
            ),
            "sandbox": forms.BooleanField(
                label=_("Use Sandbox"),
                required=False,
                initial=True,
                help_text=_("For testing"),
            ),
        }

        return fields

    def is_allowed(self, request, total=None):
        """Check if this payment method is allowed for the current request"""
        # First check parent class restrictions (date, total min/max, countries, etc.)
        if not super().is_allowed(request, total):
            return False

        # Ensure API credentials are configured
        api_key = self.settings.get("api_key")
        secret_key = self.settings.get("secret_key")
        if not api_key or not secret_key:
            return False

        # iyzico requires TRY currency
        if hasattr(request, "event") and request.event.currency != "TRY":
            return False

        return True

    def payment_form_render(self, request, total, order=None):
        """Render payment form information"""
        template = """
        <div class="alert alert-info">
            <p>{info_text}</p>
            <ul>
                <li>{secure_payment}</li>
                <li>{installment_options}</li>
                <li>{redirect_notice}</li>
            </ul>
        </div>
        """
        return template.format(
            info_text=_("Payment will be processed through iyzico payment gateway."),
            secure_payment=_("Secure payment with SSL encryption"),
            installment_options=_(
                "Installment payment options available (up to 9 installments)"
            ),
            redirect_notice=_(
                "You will be redirected to iyzico to complete your payment"
            ),
        )

    def _initialize_payment(self, request, order, payment):
        """iyzico Pay with iyzico initialize endpoint'ini çağır"""
        try:
            # iyzico konfigürasyonu
            api_key = self.settings.get("api_key")
            secret_key = self.settings.get("secret_key")
            sandbox = self.settings.get("sandbox", as_type=bool, default=True)

            if not api_key or not secret_key:
                logger.error("iyzico API key or secret key not configured")
                return None

            # Base URL
            base_url = (
                "https://sandbox-api.iyzipay.com"
                if sandbox
                else "https://api.iyzipay.com"
            )

            # Pay with iyzico initialize request
            initialize_data = {
                "locale": "tr",
                "conversationId": f"pretix_{order.code}_{payment.id}",
                "price": str(order.total),
                "paidPrice": str(order.total),
                "currency": "TRY",
                "basketId": order.code,
                "paymentGroup": "PRODUCT",
                "callbackUrl": request.build_absolute_uri(
                    reverse("plugins:pretix_iyzico:return")
                ),
                "enabledInstallments": [1, 2, 3, 6, 9],
                "buyer": {
                    "id": str(order.email),
                    "name": (
                        order.invoice_address.name_parts.get("given_name", "")
                        if order.invoice_address.name_parts
                        else order.invoice_address.name_cached or order.email
                    ),
                    "surname": (
                        order.invoice_address.name_parts.get("family_name", "")
                        if hasattr(order.invoice_address, "name_parts")
                        else ""
                    ),
                    "gsmNumber": getattr(order.invoice_address, "phone", None)
                    or "+905555555555",
                    "email": order.email,
                    "identityNumber": self._generate_identity_number(),
                    "lastLoginDate": self._format_datetime(order.datetime),
                    "registrationDate": self._format_datetime(order.datetime),
                    "registrationAddress": order.invoice_address.street or "",
                    "ip": request.META.get("REMOTE_ADDR", "127.0.0.1"),
                    "city": order.invoice_address.city or "Istanbul",
                    "country": "Turkey",
                    "zipCode": order.invoice_address.zipcode or "34000",
                },
                "shippingAddress": {
                    "contactName": (
                        order.invoice_address.name_parts.get("given_name", "")
                        if order.invoice_address.name_parts
                        else order.invoice_address.name_cached or order.email
                    ),
                    "city": order.invoice_address.city or "Istanbul",
                    "country": "Turkey",
                    "address": order.invoice_address.street or "",
                    "zipCode": order.invoice_address.zipcode or "34000",
                },
                "billingAddress": {
                    "contactName": (
                        order.invoice_address.name_parts.get("given_name", "")
                        if order.invoice_address.name_parts
                        else order.invoice_address.name_cached or order.email
                    ),
                    "city": order.invoice_address.city or "Istanbul",
                    "country": "Turkey",
                    "address": order.invoice_address.street or "",
                    "zipCode": order.invoice_address.zipcode or "34000",
                },
                "basketItems": [],
            }

            # Basket items ekle
            for position in order.positions.all():
                initialize_data["basketItems"].append(
                    {
                        "id": str(position.id),
                        "name": str(position.item.name),
                        "category1": (
                            str(position.item.category.name)
                            if position.item.category
                            else "General"
                        ),
                        "category2": "",
                        "itemType": "PHYSICAL",
                        "price": str(position.price),
                    }
                )

            # Authorization header oluştur
            random_string = self._generate_random_string(8)
            data_string = json.dumps(initialize_data, separators=(",", ":"))
            hash_string = self._create_hash_string(
                api_key, random_string, secret_key, data_string
            )

            headers = {
                "Authorization": f"IYZWS {api_key}:{hash_string}",
                "Content-Type": "application/json",
                "x-iyzi-rnd": random_string,
                "x-iyzi-client-version": "iyzipay-python-1.0.45",
            }

            # iyzico'ya POST request at
            response = requests.post(
                f"{base_url}/payment/pw/initialize",
                data=data_string,
                headers=headers,
                timeout=30,
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    # Payment'ı pending olarak işaretle
                    payment.state = "pending"
                    payment.info = json.dumps(
                        {
                            "token": result.get("token"),
                            "conversationId": initialize_data["conversationId"],
                        }
                    )
                    payment.save()

                    return result.get("payWithIyzicoPageUrl")
                else:
                    logger.error(f"iyzico initialize failed: {result}")
                    return None
            else:
                logger.error(
                    f"iyzico API error: {response.status_code} - {response.text}"
                )
                return None

        except Exception as e:
            logger.error(f"iyzico initialize error: {str(e)}")
            return None

    def _generate_random_string(self, length):
        """Random string oluştur"""
        import random
        import string

        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    def _generate_identity_number(self):
        """Generate a valid Turkish identity number for API requirements

        Note: This generates a dummy identity number for API compatibility.
        In production, you may want to collect real identity numbers if required by regulations.
        """
        import random

        # Generate 11 digit number (Turkish ID format)
        # For sandbox/testing, using a simple random 11-digit number
        return "".join([str(random.randint(0, 9)) for _ in range(11)])

    def _format_datetime(self, dt):
        """Format datetime for iyzico API

        Args:
            dt: datetime object

        Returns:
            str: Formatted datetime string in 'YYYY-MM-DD HH:MM:SS' format
        """
        if dt:
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        # Fallback to a reasonable default if datetime is None
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _create_hash_string(self, api_key, random_string, secret_key, data_string):
        """iyzico hash string oluştur"""
        hash_string = f"{api_key}{random_string}{secret_key}{data_string}"
        return base64.b64encode(
            hashlib.sha1(hash_string.encode("utf-8")).digest()
        ).decode("utf-8")

    def payment_is_valid_session(self, request):
        """Payment session valid mi kontrol et"""
        return True

    def payment_is_pending(self, payment):
        """Payment pending mi kontrol et"""
        return payment.state == "pending"

    def payment_can_retry(self, payment):
        """Payment retry edilebilir mi"""
        return payment.state in ["pending", "failed"]

    def payment_refund_supported(self, payment):
        """Refund destekleniyor mu"""
        return False  # Şimdilik desteklemiyoruz

    def payment_partial_refund_supported(self, payment):
        """Partial refund destekleniyor mu"""
        return False
