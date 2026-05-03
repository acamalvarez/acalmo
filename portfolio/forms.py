from django.forms import ModelForm
from django_recaptcha.fields import ReCaptchaField  # type: ignore[import-untyped]
from django_recaptcha.widgets import ReCaptchaV3  # type: ignore[import-untyped]

from .models.contact_models import Contact


class ContactForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message", "captcha"]
