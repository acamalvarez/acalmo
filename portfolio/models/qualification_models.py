from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property


class Qualification(models.Model):
    EDUCATION = "edu"
    WORK = "work"
    TYPE_CHOICES = {
        EDUCATION: "Education",
        WORK: "Work",
    }
    qualification_type = models.CharField(max_length=4, choices=TYPE_CHOICES, default=WORK)
    title = models.CharField()
    subtitle = models.CharField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    @cached_property
    def years(self):
        end_date = self.end_date or timezone.now()
        return f"{self.start_date.year} - {end_date.year}"
