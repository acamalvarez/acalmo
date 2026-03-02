"""Comprehensive tests for all portfolio models."""

from datetime import date
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from portfolio.models.contact_models import Contact
from portfolio.models.project_models import Project
from portfolio.models.publication_models import Publication
from portfolio.models.qualification_models import Qualification
from portfolio.models.skill_models import Skill, SubSkill


# ---------------------------------------------------------------------------
# Contact model
# ---------------------------------------------------------------------------
class ContactModelTest(TestCase):
    """Tests for the Contact model."""

    def setUp(self):
        self.contact = Contact.objects.create(
            name="Jane Doe",
            email="jane@example.com",
            subject="Hello",
            message="This is a test message.",
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.contact), "Jane Doe")

    def test_created_at_auto_set(self):
        """created_at should be populated automatically."""
        self.assertIsNotNone(self.contact.created_at)

    def test_name_max_length(self):
        self.assertEqual(Contact._meta.get_field("name").max_length, 63)

    def test_subject_max_length(self):
        self.assertEqual(Contact._meta.get_field("subject").max_length, 127)

    def test_email_field_validation(self):
        """An invalid email should fail model-level validation."""
        bad = Contact(
            name="Bad",
            email="not-an-email",
            subject="Test",
            message="msg",
        )
        with self.assertRaises(ValidationError):
            bad.full_clean()

    def test_blank_name_fails_validation(self):
        bad = Contact(name="", email="a@b.com", subject="S", message="m")
        with self.assertRaises(ValidationError):
            bad.full_clean()

    def test_blank_message_fails_validation(self):
        bad = Contact(name="A", email="a@b.com", subject="S", message="")
        with self.assertRaises(ValidationError):
            bad.full_clean()

    def test_multiple_contacts_created(self):
        Contact.objects.create(name="John", email="j@x.com", subject="Hi", message="msg")
        self.assertEqual(Contact.objects.count(), 2)


# ---------------------------------------------------------------------------
# Project model
# ---------------------------------------------------------------------------
class ProjectModelTest(TestCase):
    """Tests for the Project model."""

    def setUp(self):
        self.project = Project.objects.create(
            title="My Project",
            description="A cool project.",
            url="https://example.com",
            image="media/images/project/test.png",
            featured=True,
            active=True,
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.project), "My Project")

    def test_title_max_length(self):
        self.assertEqual(Project._meta.get_field("title").max_length, 31)

    def test_featured_default_true(self):
        p = Project.objects.create(
            title="P2",
            description="Desc",
            url="https://example.com",
            image="media/images/project/t2.png",
        )
        self.assertTrue(p.featured)

    def test_active_default_true(self):
        p = Project.objects.create(
            title="P3",
            description="Desc",
            url="https://example.com",
            image="media/images/project/t3.png",
        )
        self.assertTrue(p.active)

    def test_filter_featured(self):
        Project.objects.create(
            title="Hidden",
            description="D",
            url="https://example.com",
            image="img.png",
            featured=False,
        )
        self.assertEqual(Project.objects.filter(featured=True).count(), 1)

    def test_filter_active(self):
        Project.objects.create(
            title="Inactive",
            description="D",
            url="https://example.com",
            image="img.png",
            active=False,
        )
        self.assertEqual(Project.objects.filter(active=True).count(), 1)

    def test_image_upload_to(self):
        field = Project._meta.get_field("image")
        self.assertEqual(field.upload_to, "media/images/project")

    def test_url_field_validation(self):
        p = Project(
            title="Bad",
            description="D",
            url="not-a-url",
            image="img.png",
        )
        with self.assertRaises(ValidationError):
            p.full_clean()


# ---------------------------------------------------------------------------
# Publication model
# ---------------------------------------------------------------------------
class PublicationModelTest(TestCase):
    """Tests for the Publication model."""

    def setUp(self):
        self.pub = Publication.objects.create(
            title="My Paper",
            url="https://doi.org/10.1234/test",
            featured=True,
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.pub), "My Paper")

    def test_featured_default_true(self):
        p = Publication.objects.create(title="Another", url="https://example.com")
        self.assertTrue(p.featured)

    def test_filter_featured(self):
        Publication.objects.create(
            title="Hidden",
            url="https://example.com",
            featured=False,
        )
        self.assertEqual(Publication.objects.filter(featured=True).count(), 1)

    def test_url_field_validation(self):
        p = Publication(title="Bad", url="not-a-url")
        with self.assertRaises(ValidationError):
            p.full_clean()


# ---------------------------------------------------------------------------
# Qualification model
# ---------------------------------------------------------------------------
class QualificationModelTest(TestCase):
    """Tests for the Qualification model."""

    def setUp(self):
        self.edu = Qualification.objects.create(
            qualification_type=Qualification.EDUCATION,
            title="MSc Computer Science",
            subtitle="MIT",
            start_date=date(2018, 9, 1),
            end_date=date(2020, 6, 1),
        )
        self.work = Qualification.objects.create(
            qualification_type=Qualification.WORK,
            title="Software Engineer",
            subtitle="Google",
            start_date=date(2020, 7, 1),
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.edu), "MSc Computer Science")

    def test_type_choices(self):
        self.assertEqual(Qualification.EDUCATION, "edu")
        self.assertEqual(Qualification.WORK, "work")

    def test_default_type_is_work(self):
        q = Qualification.objects.create(
            title="Default",
            subtitle="Test",
            start_date=date(2023, 1, 1),
        )
        self.assertEqual(q.qualification_type, Qualification.WORK)

    def test_end_date_nullable(self):
        """Work entries may still be current (end_date=None)."""
        self.assertIsNone(self.work.end_date)

    def test_years_with_end_date(self):
        self.assertEqual(self.edu.years, "2018 - 2020")

    def test_years_without_end_date_uses_now(self):
        """When end_date is None, years should use the current year."""
        now_year = timezone.now().year
        expected = f"2020 - {now_year}"
        self.assertEqual(self.work.years, expected)

    def test_filter_education(self):
        qs = Qualification.objects.filter(qualification_type=Qualification.EDUCATION)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.edu)

    def test_filter_work(self):
        qs = Qualification.objects.filter(qualification_type=Qualification.WORK)
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs.first(), self.work)

    def test_qualification_type_max_length(self):
        self.assertEqual(Qualification._meta.get_field("qualification_type").max_length, 4)


# ---------------------------------------------------------------------------
# Skill model
# ---------------------------------------------------------------------------
class SkillModelTest(TestCase):
    """Tests for the Skill and SubSkill models."""

    def setUp(self):
        self.skill = Skill.objects.create(
            name="Python",
            start_date=date(2019, 1, 1),
        )
        self.sub1 = SubSkill.objects.create(skill=self.skill, name="Django")
        self.sub2 = SubSkill.objects.create(skill=self.skill, name="Flask")

    def test_str_returns_name(self):
        self.assertEqual(str(self.skill), "Python")

    def test_time_multiple_years(self):
        """A skill started many years ago should report the correct text."""
        now_year = timezone.now().year
        years = now_year - 2019
        years = max(years, 1)
        year_text = "year" if years <= 1 else "years"
        expected = f"More than {years} {year_text}"
        self.assertEqual(self.skill.time, expected)

    def test_time_less_than_one_year_clamps_to_one(self):
        """Skills started this year should still report 'More than 1 year'."""
        recent = Skill.objects.create(
            name="New",
            start_date=date.today(),
        )
        self.assertEqual(recent.time, "More than 1 year")

    def test_time_with_end_date(self):
        s = Skill.objects.create(
            name="Java",
            start_date=date(2015, 1, 1),
            end_date=date(2020, 1, 1),
        )
        self.assertEqual(s.time, "More than 5 years")

    def test_time_single_year(self):
        s = Skill.objects.create(
            name="Go",
            start_date=date(2020, 1, 1),
            end_date=date(2021, 1, 1),
        )
        self.assertEqual(s.time, "More than 1 year")

    def test_subskills_returns_related(self):
        names = sorted(s.name for s in self.skill.subskills)
        self.assertEqual(names, ["Django", "Flask"])

    def test_subskill_str(self):
        self.assertEqual(str(self.sub1), "Django")

    def test_subskill_cascade_delete(self):
        """Deleting a Skill should cascade-delete its SubSkills."""
        self.skill.delete()
        self.assertEqual(SubSkill.objects.count(), 0)

    def test_subskill_relationship(self):
        self.assertEqual(self.sub1.skill, self.skill)

    def test_end_date_nullable(self):
        s = Skill.objects.create(name="Rust", start_date=date(2022, 1, 1))
        self.assertIsNone(s.end_date)

    def test_multiple_skills_all_query(self):
        Skill.objects.create(name="C++", start_date=date(2018, 1, 1))
        self.assertEqual(Skill.objects.all().count(), 2)
