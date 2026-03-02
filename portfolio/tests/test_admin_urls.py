"""Tests for admin registrations and URL routing."""

from django.contrib.admin.sites import site as admin_site
from django.test import TestCase, override_settings
from django.urls import resolve, reverse

from portfolio.models.contact_models import Contact
from portfolio.models.project_models import Project
from portfolio.models.publication_models import Publication
from portfolio.models.qualification_models import Qualification
from portfolio.models.skill_models import Skill, SubSkill
from portfolio.views import HomeView


# ---------------------------------------------------------------------------
# Admin registration
# ---------------------------------------------------------------------------
class AdminRegistrationTest(TestCase):
    """Ensure all models are registered with the Django admin."""

    def test_contact_registered(self):
        self.assertIn(Contact, admin_site._registry)

    def test_project_registered(self):
        self.assertIn(Project, admin_site._registry)

    def test_publication_registered(self):
        self.assertIn(Publication, admin_site._registry)

    def test_qualification_registered(self):
        self.assertIn(Qualification, admin_site._registry)

    def test_skill_registered(self):
        self.assertIn(Skill, admin_site._registry)

    def test_subskill_registered(self):
        self.assertIn(SubSkill, admin_site._registry)


# ---------------------------------------------------------------------------
# URL routing
# ---------------------------------------------------------------------------
class URLRoutingTest(TestCase):
    """Tests that URL patterns resolve to the expected views."""

    def test_home_url_name(self):
        url = reverse("home")
        self.assertEqual(url, "/")

    def test_home_url_resolves_to_home_view(self):
        match = resolve("/")
        self.assertEqual(match.func.view_class, HomeView)

    def test_admin_url_resolves(self):
        url = reverse("admin:index")
        self.assertEqual(url, "/admin/")

    def test_sitemap_url_resolves(self):
        url = reverse("django.contrib.sitemaps.views.sitemap")
        self.assertEqual(url, "/sitemap.xml")
