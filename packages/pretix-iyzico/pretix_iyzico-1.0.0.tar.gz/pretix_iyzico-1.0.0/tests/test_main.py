import json
import pytest
from django_scopes import scopes_disabled
from pretix.base.models import OrderPayment
from pretix.base.payment import PaymentException
from unittest.mock import Mock, patch

from pretix_iyzico.payment import IyzicoProvider


@pytest.mark.django_db
class TestIyzicoProvider:
    """Test cases for IyzicoProvider payment provider"""

    def test_provider_identifier(self, iyzico_provider):
        """Test that provider has correct identifier"""
        assert iyzico_provider.identifier == "iyzico"

    def test_provider_verbose_name(self, iyzico_provider):
        """Test that provider has verbose name"""
        assert str(iyzico_provider.verbose_name) == "iyzico"

    def test_settings_form_fields(self, iyzico_provider):
        """Test that settings form fields are properly defined"""
        fields = iyzico_provider.settings_form_fields
        assert "api_key" in fields
        assert "secret_key" in fields
        assert "sandbox" in fields

    @scopes_disabled()
    def test_checkout_confirm_render(self, iyzico_provider, mock_request, order):
        """Test checkout confirmation render"""
        result = iyzico_provider.checkout_confirm_render(mock_request, order)
        assert result is not None
        assert "iyzico" in str(result).lower()

    def test_execute_payment_needs_user(self, iyzico_provider):
        """Test that execute_payment_needs_user is set"""
        assert iyzico_provider.execute_payment_needs_user is True

    @patch("pretix_iyzico.payment.requests.post")
    @scopes_disabled()
    def test_execute_payment_success(
        self,
        mock_post,
        iyzico_provider,
        mock_request,
        payment,
        mock_iyzico_success_response,
    ):
        """Test successful payment execution"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_iyzico_success_response
        mock_post.return_value = mock_response

        result = iyzico_provider.execute_payment(mock_request, payment)

        assert result is not None
        assert "iyzipay.com" in result
        payment.refresh_from_db()
        assert payment.state == OrderPayment.PAYMENT_STATE_PENDING

    @patch("pretix_iyzico.payment.requests.post")
    @scopes_disabled()
    def test_execute_payment_failure(
        self, mock_post, iyzico_provider, mock_request, payment
    ):
        """Test failed payment execution"""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        with pytest.raises(PaymentException):
            iyzico_provider.execute_payment(mock_request, payment)

    @patch("pretix_iyzico.payment.requests.post")
    @scopes_disabled()
    def test_initialize_payment_success(
        self,
        mock_post,
        iyzico_provider,
        mock_request,
        order,
        payment,
        mock_iyzico_success_response,
    ):
        """Test successful payment initialization"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_iyzico_success_response
        mock_post.return_value = mock_response

        result = iyzico_provider._initialize_payment(mock_request, order, payment)

        assert result is not None
        assert "iyzipay.com" in result
        mock_post.assert_called_once()

        # Verify payment was updated
        payment.refresh_from_db()
        assert payment.state == OrderPayment.PAYMENT_STATE_PENDING
        info = json.loads(payment.info)
        assert "token" in info
        assert info["token"] == "test_token_123"

    @patch("pretix_iyzico.payment.requests.post")
    @scopes_disabled()
    def test_initialize_payment_api_error(
        self, mock_post, iyzico_provider, mock_request, order, payment
    ):
        """Test payment initialization with API error"""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        result = iyzico_provider._initialize_payment(mock_request, order, payment)

        assert result is None

    @patch("pretix_iyzico.payment.requests.post")
    @scopes_disabled()
    def test_initialize_payment_iyzico_failure(
        self,
        mock_post,
        iyzico_provider,
        mock_request,
        order,
        payment,
        mock_iyzico_failure_response,
    ):
        """Test payment initialization with iyzico failure response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_iyzico_failure_response
        mock_post.return_value = mock_response

        result = iyzico_provider._initialize_payment(mock_request, order, payment)

        assert result is None

    @scopes_disabled()
    def test_initialize_payment_missing_credentials(
        self, event, mock_request, order, payment
    ):
        """Test payment initialization with missing credentials"""
        provider = IyzicoProvider(event)
        # Don't set API credentials

        result = provider._initialize_payment(mock_request, order, payment)

        assert result is None

    def test_generate_random_string(self, iyzico_provider):
        """Test random string generation"""
        result = iyzico_provider._generate_random_string(8)
        assert len(result) == 8
        assert result.isalnum()

    def test_create_hash_string(self, iyzico_provider):
        """Test hash string creation"""
        api_key = "test_api_key"
        random_string = "abc123"
        secret_key = "test_secret"
        data = '{"test":"data"}'

        result = iyzico_provider._create_hash_string(
            api_key, random_string, secret_key, data
        )

        assert result is not None
        assert isinstance(result, str)
        # Base64 encoded strings should not contain certain characters
        assert " " not in result

    def test_payment_is_valid_session(self, iyzico_provider, mock_request):
        """Test payment session validation"""
        result = iyzico_provider.payment_is_valid_session(mock_request)
        assert result is True

    @scopes_disabled()
    def test_payment_is_pending(self, iyzico_provider, payment):
        """Test payment pending check"""
        payment.state = OrderPayment.PAYMENT_STATE_PENDING
        payment.save()
        assert iyzico_provider.payment_is_pending(payment) is True

        payment.state = OrderPayment.PAYMENT_STATE_CONFIRMED
        payment.save()
        assert iyzico_provider.payment_is_pending(payment) is False

    @scopes_disabled()
    def test_payment_can_retry(self, iyzico_provider, payment):
        """Test payment retry check"""
        payment.state = OrderPayment.PAYMENT_STATE_PENDING
        payment.save()
        assert iyzico_provider.payment_can_retry(payment) is True

        payment.state = OrderPayment.PAYMENT_STATE_FAILED
        payment.save()
        assert iyzico_provider.payment_can_retry(payment) is True

        payment.state = OrderPayment.PAYMENT_STATE_CONFIRMED
        payment.save()
        assert iyzico_provider.payment_can_retry(payment) is False

    @scopes_disabled()
    def test_payment_refund_supported(self, iyzico_provider, payment):
        """Test refund support check"""
        assert iyzico_provider.payment_refund_supported(payment) is False

    @scopes_disabled()
    def test_payment_partial_refund_supported(self, iyzico_provider, payment):
        """Test partial refund support check"""
        assert iyzico_provider.payment_partial_refund_supported(payment) is False

    @patch("pretix_iyzico.payment.requests.post")
    @scopes_disabled()
    def test_initialize_payment_basket_items(
        self,
        mock_post,
        iyzico_provider,
        mock_request,
        order,
        payment,
        mock_iyzico_success_response,
    ):
        """Test that basket items are properly included in payment request"""
        from pretix.base.models import Item, ItemCategory, OrderPosition

        # Create test items
        category = ItemCategory.objects.create(event=order.event, name="Test Category")
        item = Item.objects.create(
            event=order.event, name="Test Ticket", default_price=100, category=category
        )
        OrderPosition.objects.create(order=order, item=item, price=100)

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_iyzico_success_response
        mock_post.return_value = mock_response

        result = iyzico_provider._initialize_payment(mock_request, order, payment)

        assert result is not None

        # Verify the API was called with basket items
        call_args = mock_post.call_args
        data = json.loads(call_args[1]["data"])
        assert "basketItems" in data
        assert len(data["basketItems"]) > 0
        assert data["basketItems"][0]["name"] == "Test Ticket"

    def test_sandbox_url_configuration(self, iyzico_provider):
        """Test that sandbox mode uses correct URL"""
        assert iyzico_provider.settings.get("sandbox", as_type=bool) is True

    @patch("pretix_iyzico.payment.requests.post")
    @scopes_disabled()
    def test_initialize_payment_uses_sandbox_url(
        self,
        mock_post,
        iyzico_provider,
        mock_request,
        order,
        payment,
        mock_iyzico_success_response,
    ):
        """Test that sandbox URL is used when sandbox mode is enabled"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_iyzico_success_response
        mock_post.return_value = mock_response

        iyzico_provider._initialize_payment(mock_request, order, payment)

        call_args = mock_post.call_args
        assert "sandbox-api.iyzipay.com" in call_args[0][0]

    @patch("pretix_iyzico.payment.requests.post")
    @scopes_disabled()
    def test_initialize_payment_uses_production_url(
        self,
        mock_post,
        iyzico_provider,
        mock_request,
        order,
        payment,
        mock_iyzico_success_response,
    ):
        """Test that production URL is used when sandbox mode is disabled"""
        iyzico_provider.settings.set("sandbox", False)

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_iyzico_success_response
        mock_post.return_value = mock_response

        iyzico_provider._initialize_payment(mock_request, order, payment)

        call_args = mock_post.call_args
        assert "sandbox" not in call_args[0][0]
        assert "api.iyzipay.com" in call_args[0][0]
