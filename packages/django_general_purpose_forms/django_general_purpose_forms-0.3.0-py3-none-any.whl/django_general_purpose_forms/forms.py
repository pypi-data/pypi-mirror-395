# Django
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _


class AbstractGeneralPurposeForm(forms.Form):
    """
    Abstract base class for generic-purpose forms.
    Get an instance of an object.
    """

    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields |= {
            "ct": forms.CharField(widget=forms.HiddenInput()),
            "id": forms.CharField(widget=forms.HiddenInput()),
            "field_that_must_stay_empty": forms.CharField(
                widget=forms.HiddenInput(), required=False
            ),
        }
        self.fields["ct"].initial = ContentType.objects.get_for_model(instance).id
        self.fields["id"].initial = instance.id
        self.object = instance

    # Validators

    def field_that_must_stay_empty(self):
        field_that_must_stay_empty = self.cleaned_data.get("field_that_must_stay_empty")
        if field_that_must_stay_empty:
            raise forms.ValidationError("Honey pot field must be empty")
        return field_that_must_stay_empty

    # Send-email-related methods

    def get_email_address(self):
        raise NotImplementedError(
            _("You need to implement this yourself. Do not forget to return a list!")
        )

    def get_subject(self):
        raise NotImplementedError(_("You need to implement this yourself."))

    def get_from_email(self):
        raise NotImplementedError(_("You need to implement this yourself."))

    def get_txt_message(self):
        raise NotImplementedError(_("You need to implement this yourself."))

    def get_html_message(self):
        raise NotImplementedError(_("You need to implement this yourself."))

    def get_fail_silently(self):
        return False

    def send_dgpf_form_by_email(self):
        send_mail(
            subject=self.get_subject(),
            message=self.get_txt_message(),
            from_email=self.get_from_email(),
            recipient_list=self.get_email_address(),
            fail_silently=self.get_fail_silently(),
            html_message=self.get_html_message(),
        )

    # Save-the-form-in-db-related methods

    def save_dgpf_form(self):
        # Local application / specific library imports
        from .models import SentForm

        SentForm.objects.create(
            content_type=ContentType.objects.get_for_model(self.object),
            object_id=self.object.id,
            content=self.get_txt_message(),
        )

    # What to do when the form is valid

    def save(self, form):
        raise NotImplementedError(
            _(
                "You need to implement this yourself. For example, you can call `send_dgpf_form_by_email`."
            )
        )
