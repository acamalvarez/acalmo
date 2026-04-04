from django.conf import settings
from django.forms import ModelForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

from .models.contact_models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        if not settings.DEBUG:
            self.fields["captcha"] = ReCaptchaField(widget=ReCaptchaV3)

