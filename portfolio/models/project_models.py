from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=31)
    description = models.TextField()
    url = models.URLField()
    image = models.ImageField(upload_to="media/images/project")
    featured = models.BooleanField(default=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title
