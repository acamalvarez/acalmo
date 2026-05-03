"""Comprehensive tests for the ContactForm."""

from unittest.mock import patch

from django.test import TestCase, override_settings

from portfolio.forms import ContactForm


class ContactFormValidTest(TestCase):
    """Tests that valid data passes form validation."""

    @patch("django_recaptcha.fields.ReCaptchaField.clean")
    def test_valid_data(self, mock_clean):
        mock_clean.return_value = "PASSED"
        form = ContactForm(
            data={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "subject": "Hello",
                "message": "This is a test message.",
                "captcha": "PASSED",
            }
        )
        self.assertTrue(form.is_valid())

    @patch("django_recaptcha.fields.ReCaptchaField.clean")
    def test_form_saves_to_db(self, mock_clean):
        mock_clean.return_value = "PASSED"
        form = ContactForm(
            data={
                "name": "Jane Doe",
                "email": "jane@example.com",
                "subject": "Hello",
                "message": "Test message.",
                "captcha": "PASSED",
            }
        )
        self.assertTrue(form.is_valid())
        contact = form.save()
        self.assertEqual(contact.name, "Jane Doe")
        self.assertEqual(contact.email, "jane@example.com")
        self.assertEqual(contact.subject, "Hello")
        self.assertEqual(contact.message, "Test message.")
        self.assertIsNotNone(contact.pk)


class ContactFormInvalidTest(TestCase):
    """Tests that missing / invalid data is properly caught."""

    def test_missing_name(self):
        form = ContactForm(
            data={
                "name": "",
                "email": "a@b.com",
                "subject": "S",
                "message": "m",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_email(self):
        form = ContactForm(
            data={
                "name": "A",
                "email": "",
                "subject": "S",
                "message": "m",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_invalid_email(self):
        form = ContactForm(
            data={
                "name": "A",
                "email": "not-an-email",
                "subject": "S",
                "message": "m",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_missing_subject(self):
        form = ContactForm(
            data={
                "name": "A",
                "email": "a@b.com",
                "subject": "",
                "message": "m",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("subject", form.errors)

    def test_missing_message(self):
        form = ContactForm(
            data={
                "name": "A",
                "email": "a@b.com",
                "subject": "S",
                "message": "",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)

    def test_empty_form(self):
        form = ContactForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 5)  # all five fields required

    def test_name_exceeds_max_length(self):
        form = ContactForm(
            data={
                "name": "A" * 64,  # max_length=63
                "email": "a@b.com",
                "subject": "S",
                "message": "m",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_subject_exceeds_max_length(self):
        form = ContactForm(
            data={
                "name": "A",
                "email": "a@b.com",
                "subject": "S" * 128,  # max_length=127
                "message": "m",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("subject", form.errors)


class ContactFormFieldsTest(TestCase):
    """Tests that the form exposes the expected fields."""

    def test_form_fields(self):
        form = ContactForm()
        expected = {"name", "email", "subject", "message", "captcha"}
        self.assertEqual(set(form.fields.keys()), expected)

    def test_created_at_not_in_fields(self):
        """created_at is auto-set and should not appear in the form."""
        form = ContactForm()
        self.assertNotIn("created_at", form.fields)
