from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property


class Contact(models.Model):
    name = models.CharField(max_length=63)
    email = models.EmailField()
    subject = models.CharField(max_length=127)
    message = models.TextField()

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=31)
    description = models.TextField()
    url = models.URLField()
    image = models.ImageField(upload_to="media/images/project")
    featured = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Publication(models.Model):
    title = models.CharField()
    url = models.URLField()
    featured = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Qualification(models.Model):
    EDUCATION = "edu"
    WORK = "work"
    TYPE_CHOICES = {
        EDUCATION: "Education",
        WORK: "Work",
    }
    qualification_type = models.CharField(
        max_length=4, choices=TYPE_CHOICES, default=WORK
    )
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


class Skill(models.Model):
    name = models.CharField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    @cached_property
    def time(self):
        end_date = self.end_date or timezone.now()
        number_of_years = end_date.year - self.start_date.year
        number_of_years = 1 if number_of_years < 1 else number_of_years
        year_text = "year" if number_of_years <= 1 else "years"
        return f"More than {number_of_years} {year_text}"

    @cached_property
    def subskills(self):
        return self.subskill_set.all()


class SubSkill(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    name = models.CharField()

    def __str__(self) -> str:
        return self.name
