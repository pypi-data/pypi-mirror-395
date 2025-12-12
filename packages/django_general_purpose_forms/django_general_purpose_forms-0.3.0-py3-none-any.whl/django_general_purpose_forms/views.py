# Django
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView


class HandleFormView(FormView):
    def get_template_names(self):
        return (
            "django_general_purpose_forms/" + self.form_config["template_name"]
            if "template_name" in self.form_config
            else "django_general_purpose_forms/form.html"
        )

    def get_form_class(self):
        """
        Returns the form class to use in this view from the DJANGO_GENERAL_PURPOSE_FORMS_CONFIG setting (a dictionary with form names as keys and form class paths as values).
        Return the actual form class from the string path using the import_string function.
        """
        try:
            self.form_config = settings.DJANGO_GENERAL_PURPOSE_FORMS_CONFIG[
                self.kwargs["form_name"]
            ]
            form_class_str = self.form_config["form_path"]
        except KeyError:
            raise ValueError(
                _(
                    f"Form {self.kwargs['form_name']} not found in DJANGO_GENERAL_PURPOSE_FORMS_CONFIG."
                )
            ) from KeyError

        form_class = import_string(form_class_str)
        return form_class

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view, from the ct and id values in POST data.
        ct helps us retrieve the model (from the django content type table), and id is the primary key of the model instance.
        """
        if form_class is None:
            form_class = self.get_form_class()
        ct = ContentType.objects.get(id=self.request.POST["ct"])
        id = self.request.POST["id"]
        self.object = ct.get_object_for_this_type(id=id)
        return form_class(self.object, **self.get_form_kwargs())

    def form_valid(self, form):
        """
        If the form is valid, "save" the form and redirect to the success URL.
        """
        form.save(self.request)
        return super().form_valid(form)

    def get_success_url(self):
        """
        Try to return the success url with the pk of the object, if it fails, return the success url without any arguments.
        This allows us to use the success url with or without a pk, depending on the use case, without having to define two different urls.
        """
        try:
            return reverse(
                self.form_config["success_url"], kwargs={"pk": self.object.pk}
            )
        except:  # noqa
            try:
                return reverse(self.form_config["success_url"])
            except:  # noqa
                try:
                    return getattr(self.object, self.form_config["success_url"])()
                except:  # noqa
                    return getattr(self.object, self.form_config["success_url"])
