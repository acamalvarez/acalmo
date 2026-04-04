"""Comprehensive tests for the HomeView."""

from datetime import date
from unittest.mock import patch

from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django_recaptcha.client import RecaptchaResponse

from portfolio.models.contact_models import Contact
from portfolio.models.project_models import Project
from portfolio.models.publication_models import Publication
from portfolio.models.qualification_models import Qualification
from portfolio.models.skill_models import Skill, SubSkill


# ---------------------------------------------------------------------------
# Helper mixin to seed the database for view tests
# ---------------------------------------------------------------------------
class SeedDataMixin:
    """Creates a standard set of database objects for view tests."""

    @classmethod
    def setUpTestData(cls):
        # Projects — one featured, one not
        cls.featured_project = Project.objects.create(
            title="Featured",
            description="A featured project.",
            url="https://example.com/featured",
            image="media/images/project/f.png",
            featured=True,
        )
        cls.hidden_project = Project.objects.create(
            title="Hidden",
            description="A hidden project.",
            url="https://example.com/hidden",
            image="media/images/project/h.png",
            featured=False,
        )

        # Publications — one featured, one not
        cls.featured_pub = Publication.objects.create(
            title="Featured Publication",
            url="https://doi.org/10.1234/featured",
            featured=True,
        )
        cls.hidden_pub = Publication.objects.create(
            title="Hidden Publication",
            url="https://doi.org/10.1234/hidden",
            featured=False,
        )

        # Skills
        cls.skill = Skill.objects.create(name="Python", start_date=date(2019, 1, 1))
        SubSkill.objects.create(skill=cls.skill, name="Django")

        # Qualifications — one education, one work
        cls.education = Qualification.objects.create(
            qualification_type=Qualification.EDUCATION,
            title="MSc CS",
            subtitle="MIT",
            start_date=date(2018, 9, 1),
            end_date=date(2020, 6, 1),
        )
        cls.work = Qualification.objects.create(
            qualification_type=Qualification.WORK,
            title="Software Engineer",
            subtitle="Google",
            start_date=date(2020, 7, 1),
        )


# ---------------------------------------------------------------------------
# GET tests
# ---------------------------------------------------------------------------
@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
)
class HomeViewGETTest(SeedDataMixin, TestCase):
    """Tests for GET requests to the home page."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("home")

    def test_status_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "portfolio/index.html")

    def test_context_contains_projects(self):
        response = self.client.get(self.url)
        self.assertIn("projects", response.context)

    def test_context_projects_only_featured(self):
        response = self.client.get(self.url)
        projects = list(response.context["projects"])
        self.assertIn(self.featured_project, projects)
        self.assertNotIn(self.hidden_project, projects)

    def test_context_contains_publications(self):
        response = self.client.get(self.url)
        self.assertIn("publications", response.context)

    def test_context_publications_only_featured(self):
        response = self.client.get(self.url)
        pubs = list(response.context["publications"])
        self.assertIn(self.featured_pub, pubs)
        self.assertNotIn(self.hidden_pub, pubs)

    def test_context_contains_skills(self):
        response = self.client.get(self.url)
        self.assertIn("skills", response.context)
        self.assertEqual(response.context["skills"].count(), 1)

    def test_context_contains_educations(self):
        response = self.client.get(self.url)
        self.assertIn("educations", response.context)
        educations = list(response.context["educations"])
        self.assertIn(self.education, educations)
        self.assertNotIn(self.work, educations)

    def test_context_contains_works(self):
        response = self.client.get(self.url)
        self.assertIn("works", response.context)
        works = list(response.context["works"])
        self.assertIn(self.work, works)
        self.assertNotIn(self.education, works)

    def test_context_contains_form(self):
        response = self.client.get(self.url)
        self.assertIn("form", response.context)

    def test_empty_database_returns_200(self):
        """The view should still render when the database is empty."""
        Project.objects.all().delete()
        Publication.objects.all().delete()
        Skill.objects.all().delete()
        Qualification.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


# ---------------------------------------------------------------------------
# POST tests — valid form
# ---------------------------------------------------------------------------
@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class HomeViewValidPOSTTest(SeedDataMixin, TestCase):
    """Tests for a valid POST (contact-form submission) on the home page."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("home")
        self.valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "subject": "Test Subject",
            "message": "Hello, this is a test.",
            "captcha": "PASSED",
        }

    @patch("django_recaptcha.fields.client.submit")
    @patch("portfolio.views.send_mail")
    def test_valid_post_redirects(self, mock_send_mail, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True, extra_data={"score": 0.9})
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    @patch("django_recaptcha.fields.client.submit")
    @patch("portfolio.views.send_mail")
    def test_valid_post_saves_contact(self, mock_send_mail, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True, extra_data={"score": 0.9})
        self.client.post(self.url, data=self.valid_data)
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john@example.com")

    @patch("django_recaptcha.fields.client.submit")
    @patch("portfolio.views.send_mail")
    def test_valid_post_sends_email(self, mock_send_mail, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True, extra_data={"score": 0.9})
        self.client.post(self.url, data=self.valid_data)
        mock_send_mail.assert_called_once()
        call_kwargs = mock_send_mail.call_args
        self.assertEqual(call_kwargs[1]["subject"], "Test Subject")
        self.assertIn("john@example.com", call_kwargs[1]["message"])
        self.assertIn("John Doe", call_kwargs[1]["message"])
        self.assertIn("Hello, this is a test.", call_kwargs[1]["message"])

    @patch("django_recaptcha.fields.client.submit")
    @patch("portfolio.views.send_mail")
    def test_valid_post_sets_success_message(self, mock_send_mail, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True, extra_data={"score": 0.9})
        response = self.client.post(self.url, data=self.valid_data, follow=True)
        msgs = list(response.context["messages"])
        self.assertEqual(len(msgs), 1)
        self.assertEqual(str(msgs[0]), "Message sent successfully!")

    @patch("django_recaptcha.fields.client.submit")
    @patch("portfolio.views.send_mail")
    def test_valid_post_email_failure_propagates(self, mock_send_mail, mocked_submit):
        """Test that if send_mail raises an exception, the exception propagates."""
        from smtplib import SMTPException

        mocked_submit.return_value = RecaptchaResponse(is_valid=True, extra_data={"score": 0.9})
        mock_send_mail.side_effect = SMTPException("SMTP server disconnected")

        with self.assertRaises(SMTPException):
            self.client.post(self.url, data=self.valid_data)

        # Ensure contact wasn't saved because exception aborted the transaction/flow
        self.assertEqual(Contact.objects.count(), 0)


# ---------------------------------------------------------------------------
# POST tests — invalid form
# ---------------------------------------------------------------------------
@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
)
class HomeViewInvalidPOSTTest(SeedDataMixin, TestCase):
    """Tests that invalid POSTs re-render the page with errors."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("home")

    def test_empty_post_returns_200(self):
        """An invalid form should re-render (200), not redirect."""
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, 200)

    def test_empty_post_does_not_save(self):
        self.client.post(self.url, data={})
        self.assertEqual(Contact.objects.count(), 0)

    def test_invalid_email_returns_errors(self):
        response = self.client.post(
            self.url,
            data={
                "name": "A",
                "email": "bad",
                "subject": "S",
                "message": "m",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())
        self.assertIn("email", response.context["form"].errors)

    def test_missing_name_returns_errors(self):
        response = self.client.post(
            self.url,
            data={
                "name": "",
                "email": "a@b.com",
                "subject": "S",
                "message": "m",
            },
        )
        self.assertIn("name", response.context["form"].errors)

    def test_context_still_populated_on_invalid_post(self):
        """Even on a failed POST, the page context should contain all data."""
        response = self.client.post(self.url, data={})
        self.assertIn("projects", response.context)
        self.assertIn("publications", response.context)
        self.assertIn("skills", response.context)
        self.assertIn("educations", response.context)
        self.assertIn("works", response.context)

    @patch("django_recaptcha.fields.client.submit")
    def test_recaptcha_failure_rejects_form(self, mocked_submit):
        """A failed reCAPTCHA should reject the form and not save a Contact."""
        mocked_submit.return_value = RecaptchaResponse(is_valid=False)
        valid_data = {
            "name": "Bot",
            "email": "bot@example.com",
            "subject": "Spam",
            "message": "Buy now!",
            "captcha": "FAILED",
        }
        with self.assertLogs("django_recaptcha.fields", level="WARNING"):
            response = self.client.post(reverse("home"), data=valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("captcha", response.context["form"].errors)
        self.assertEqual(Contact.objects.count(), 0)

    @patch("django_recaptcha.fields.client.submit")
    def test_low_recaptcha_score_rejects_form(self, mocked_submit):
        """A reCAPTCHA v3 score below the threshold should reject the form."""
        mocked_submit.return_value = RecaptchaResponse(is_valid=True, extra_data={"score": 0.1})
        valid_data = {
            "name": "Bot",
            "email": "bot@example.com",
            "subject": "Spam",
            "message": "Buy now!",
            "captcha": "LOW_SCORE",
        }
        with self.assertLogs("django_recaptcha.fields", level="WARNING"):
            response = self.client.post(reverse("home"), data=valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("captcha", response.context["form"].errors)
        self.assertEqual(Contact.objects.count(), 0)

