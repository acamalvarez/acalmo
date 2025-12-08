from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PortfolioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ["home"]

    def location(self, item):
        if item == "home":
            return reverse("home")

    def lastmod(self, item):
        # Return None for static content
        return None
