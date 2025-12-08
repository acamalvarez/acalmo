from django.contrib.sitemaps import Sitemap
from django.templatetags.static import static
from django.urls import reverse


class PortfolioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return ["home", "resume"]

    def location(self, item):
        if item == "home":
            return reverse("home")
        elif item == "resume":
            return static("pdf/resume-acam.pdf")

    def lastmod(self, item):
        # Return None for static content
        return None
