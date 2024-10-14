from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http.response import HttpResponse as HttpResponse
from django.views.generic.edit import FormView

from .forms import ContactForm
from .models import Project, Publication, Qualification, Skill


class HomeView(FormView):
    template_name = "portfolio/index.html"
    form_class = ContactForm
    success_url = "/"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["projects"] = Project.objects.filter(featured=True)
        context["publications"] = Publication.objects.filter(featured=True)
        context["skills"] = Skill.objects.all()
        context["educations"] = Qualification.objects.filter(
            qualification_type=Qualification.EDUCATION
        )
        context["works"] = Qualification.objects.filter(
            qualification_type=Qualification.WORK
        )
        return context

    def form_valid(self, form: Any) -> HttpResponse:
        message = form.cleaned_data["message"]
        email = form.cleaned_data["email"]
        message = f"From: {email}\n{message}"

        send_mail(
            subject=form.cleaned_data["subject"],
            message=message,
            from_email="",
            recipient_list=[settings.EMAIL_HOST_USER],
        )

        form.save()

        return super().form_valid(form)
