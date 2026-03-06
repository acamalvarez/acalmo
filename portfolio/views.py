from typing import Any

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic.edit import FormView

from .forms import ContactForm
from .models.project_models import Project
from .models.publication_models import Publication
from .models.qualification_models import Qualification
from .models.skill_models import Skill


class HomeView(FormView):
    template_name = "portfolio/index.html"
    form_class = ContactForm
    success_url = "/"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(featured=True)
        context["publications"] = Publication.objects.filter(featured=True)
        context["skills"] = Skill.objects.prefetch_related("subskill_set").all()
        context["educations"] = Qualification.objects.filter(qualification_type=Qualification.EDUCATION)
        context["works"] = Qualification.objects.filter(qualification_type=Qualification.WORK)
        return context

    def form_valid(self, form: Any) -> HttpResponse:
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]
        name = form.cleaned_data["name"]

        email_message = f"From: {email}\n{name}\n{message}"

        send_mail(
            subject=form.cleaned_data["subject"],
            message=email_message,
            from_email="",
            recipient_list=[settings.EMAIL_HOST_USER],
        )

        form.save()

        messages.add_message(self.request, messages.SUCCESS, "Message sent successfully!")

        return super().form_valid(form)
