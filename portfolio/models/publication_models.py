from django.db import models


class Publication(models.Model):
    title = models.CharField()
    url = models.URLField()
    featured = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
