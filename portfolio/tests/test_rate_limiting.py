"""Tests for rate limiting on the contact form.

Rate limiting is implicitly controlled by the cache backend:
- LocMemCache / Redis / Memcached → rate limiting is active
- DummyCache (development default) → rate limiting is a no-op
"""

from unittest.mock import MagicMock, patch

from django.test import Client, TestCase, override_settings
from django.urls import reverse

LOCMEM_CACHE = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "rate-limit-tests",
    }
}

DUMMY_CACHE = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}


# ---------------------------------------------------------------------------
# Contact form rate limiting (real cache → active)
# ---------------------------------------------------------------------------
@override_settings(CACHES=LOCMEM_CACHE, RECAPTCHA_TESTING=True)
class ContactFormRateLimitTest(TestCase):
    """With a real cache backend the 6th POST within one minute is blocked."""

    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse("home")
        self.valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "message": "Hello, this is a test.",
            "g-recaptcha-response": "PASSED",
        }

    @patch("django_recaptcha.fields.ReCaptchaField.clean")
    @patch("portfolio.views.send_mail")
    def test_rate_limit_allows_first_five_requests(self, mock_send_mail: MagicMock, mock_clean: MagicMock) -> None:
        """The first 5 POST requests should succeed (302 redirect)."""
        mock_clean.return_value = "PASSED"
        for _ in range(5):
            response = self.client.post(self.url, data=self.valid_data)
            self.assertEqual(response.status_code, 302, "Expected 302 redirect for allowed request")

    @patch("django_recaptcha.fields.ReCaptchaField.clean")
    @patch("portfolio.views.send_mail")
    def test_rate_limit_blocks_sixth_request(self, mock_send_mail: MagicMock, mock_clean: MagicMock) -> None:
        """The 6th POST within the same minute should be blocked."""
        mock_clean.return_value = "PASSED"
        for _ in range(5):
            self.client.post(self.url, data=self.valid_data)

        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 403)

    def test_get_requests_are_not_rate_limited(self) -> None:
        """GET requests should never be rate-limited."""
        for _ in range(10):
            response = self.client.get(self.url)
            self.assertEqual(response.status_code, 200)


# ---------------------------------------------------------------------------
# DummyCache → rate limiting is effectively disabled
# ---------------------------------------------------------------------------
@override_settings(CACHES=DUMMY_CACHE, RECAPTCHA_TESTING=True)
class RateLimitWithDummyCacheTest(TestCase):
    """With DummyCache (dev default) no requests are ever blocked."""

    def setUp(self) -> None:
        self.client = Client()
        self.url = reverse("home")
        self.valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "message": "Hello, this is a test.",
            "g-recaptcha-response": "PASSED",
        }

    @patch("django_recaptcha.fields.ReCaptchaField.clean")
    @patch("portfolio.views.send_mail")
    def test_no_rate_limit_with_dummy_cache(self, mock_send_mail: MagicMock, mock_clean: MagicMock) -> None:
        """All 10 POST requests should succeed when using DummyCache."""
        mock_clean.return_value = "PASSED"
        for i in range(10):
            response = self.client.post(self.url, data=self.valid_data)
            self.assertEqual(
                response.status_code,
                302,
                f"Request {i + 1} was unexpectedly blocked",
            )
