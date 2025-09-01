from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property


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
