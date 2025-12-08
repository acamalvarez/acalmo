from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from portfolio.sitemaps import PortfolioSitemap

sitemaps = {
    'portfolio': PortfolioSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("portfolio.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
]
