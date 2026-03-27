"""Tests for the PortfolioSitemap."""

from django.test import TestCase, override_settings
from django.urls import reverse

from portfolio.sitemaps import PortfolioSitemap


class PortfolioSitemapTest(TestCase):
    """Tests for the PortfolioSitemap configuration."""

    def setUp(self):
        self.sitemap = PortfolioSitemap()

    def test_items_returns_home(self):
        self.assertEqual(self.sitemap.items(), ["home"])

    def test_changefreq(self):
        self.assertEqual(self.sitemap.changefreq, "weekly")

    def test_priority(self):
        self.assertEqual(self.sitemap.priority, 0.8)

    def test_protocol(self):
        self.assertEqual(self.sitemap.protocol, "https")

    def test_location_home(self):
        self.assertEqual(self.sitemap.location("home"), reverse("home"))


@override_settings(
    CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}},
)
class SitemapXMLEndpointTest(TestCase):
    """Tests that the sitemap.xml endpoint is reachable and well-formed."""

    def test_sitemap_xml_status_200(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)

    def test_sitemap_xml_content_type(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response["Content-Type"], "application/xml")

    def test_sitemap_xml_contains_home_url(self):
        response = self.client.get("/sitemap.xml")
        content = response.content.decode()
        self.assertIn("<loc>", content)
