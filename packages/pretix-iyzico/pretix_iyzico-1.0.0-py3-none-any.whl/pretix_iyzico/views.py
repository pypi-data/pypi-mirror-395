import base64
import hashlib
import json
import logging
import requests
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from pretix.base.models import OrderPayment
from pretix.base.payment import PaymentException

logger = logging.getLogger(__name__)


def return_view(request):
    """iyzico'dan dönen kullanıcıyı işle"""
    try:
        token = request.GET.get("token")
        if not token:
            logger.error("No token in return URL")
            return HttpResponseBadRequest("Missing token")

        # Payment'ı bul
        payment = None
        for p in OrderPayment.objects.filter(provider="iyzico", state="pending"):
            try:
                info = json.loads(p.info or "{}")
                if info.get("token") == token:
                    payment = p
                    break
            except (json.JSONDecodeError, KeyError):
                continue

        if not payment:
            logger.error(f"Payment not found for token: {token}")
            return HttpResponseBadRequest("Payment not found")

        order = payment.order

        # iyzico'dan payment durumunu kontrol et
        result = _check_payment_status(payment, token)

        if result and result.get("status") == "success":
            try:
                payment.confirm()
                messages.success(request, "Payment completed successfully!")
                return HttpResponseRedirect(
                    reverse(
                        "presale:event.order",
                        kwargs={
                            "event": order.event.slug,
                            "organizer": order.event.organizer.slug,
                            "order": order.code,
                            "secret": order.secret,
                        },
                    )
                )
            except PaymentException as e:
                logger.error(f"Payment confirmation failed: {str(e)}")
                messages.error(request, f"Payment confirmation failed: {str(e)}")
        else:
            logger.error(f"Payment failed: {result}")
            payment.fail()
            messages.error(request, "Payment failed or was cancelled.")

        return HttpResponseRedirect(
            reverse(
                "presale:event.order.pay",
                kwargs={
                    "event": order.event.slug,
                    "organizer": order.event.organizer.slug,
                    "order": order.code,
                    "secret": order.secret,
                },
            )
        )

    except Exception as e:
        logger.error(f"Return view error: {str(e)}")
        return HttpResponseBadRequest("Error processing return")


@csrf_exempt
@require_http_methods(["POST"])
def webhook_view(request):
    """iyzico webhook endpoint'i"""
    try:
        # Request body'yi al
        body = request.body.decode("utf-8")
        if not body:
            return HttpResponseBadRequest("Empty body")

        # JSON parse et
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        # Token'ı al
        token = data.get("token")
        if not token:
            return HttpResponseBadRequest("Missing token")

        # Payment'ı bul
        payment = None
        for p in OrderPayment.objects.filter(provider="iyzico", state="pending"):
            try:
                info = json.loads(p.info or "{}")
                if info.get("token") == token:
                    payment = p
                    break
            except (json.JSONDecodeError, KeyError):
                continue

        if not payment:
            logger.error(f"Payment not found for webhook token: {token}")
            return HttpResponseBadRequest("Payment not found")

        # iyzico'dan payment durumunu kontrol et
        result = _check_payment_status(payment, token)

        if result and result.get("status") == "success":
            try:
                payment.confirm()
                logger.info(f"Payment {payment.id} confirmed via webhook")
                return HttpResponse("OK")
            except PaymentException as e:
                logger.error(f"Payment confirmation failed in webhook: {str(e)}")
                return HttpResponseBadRequest("Payment confirmation failed")
        else:
            logger.error(f"Payment failed in webhook: {result}")
            payment.fail()
            return HttpResponse("Payment failed")

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return HttpResponseBadRequest("Webhook error")


def _check_payment_status(payment, token):
    """iyzico'dan payment durumunu kontrol et"""
    try:
        # Provider settings'lerini al
        provider = payment.order.event.get_payment_providers().get("iyzico")
        if not provider:
            return None

        api_key = provider.settings.get("api_key")
        secret_key = provider.settings.get("secret_key")
        sandbox = provider.settings.get("sandbox", True)

        if not api_key or not secret_key:
            logger.error("iyzico API key or secret key not configured")
            return None

        # Base URL
        base_url = (
            "https://sandbox-api.iyzipay.com" if sandbox else "https://api.iyzipay.com"
        )

        # Payment status request
        status_data = {
            "locale": "tr",
            "conversationId": f"pretix_{payment.order.code}_{payment.id}",
            "token": token,
        }

        # Authorization header oluştur
        import random
        import string

        random_string = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        data_string = json.dumps(status_data, separators=(",", ":"))
        hash_string = _create_hash_string(
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
            f"{base_url}/payment/pw/status",
            data=data_string,
            headers=headers,
            timeout=30,
        )

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(
                f"iyzico status API error: {response.status_code} - {response.text}"
            )
            return None

    except Exception as e:
        logger.error(f"iyzico status check error: {str(e)}")
        return None


def _create_hash_string(api_key, random_string, secret_key, data_string):
    """iyzico hash string oluştur"""
    hash_string = f"{api_key}{random_string}{secret_key}{data_string}"
    return base64.b64encode(hashlib.sha1(hash_string.encode("utf-8")).digest()).decode(
        "utf-8"
    )
