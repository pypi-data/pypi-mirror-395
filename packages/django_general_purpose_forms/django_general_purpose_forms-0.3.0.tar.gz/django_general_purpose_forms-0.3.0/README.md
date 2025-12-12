# Django general-purpose forms

Create forms, bind them to arbitrary objects, and add specific behaviors on submit with ease!

This package will handle the generic foreign key part of your forms, and provide a view tied to an url to submit your forms to. It can also be used to save your forms to the database (all content goes in one field), and send an email to one or more adresses related to your arbitrary objects.

You can still use your own views to handle form submission if you want to, for example by creating a `Mixin`  (not included in this package).

## Requirements
Tested with Python>=3.12 and Django>=3.2.

*Also tested from an apphook (django-cms).*

## Install

1) Install the package
  ```sh
  pip install django-general-purpose-form
  ```
2) Add it to your `INSTALLED_APPS`
  ```python
      "django_general_purpose_forms",
  ```
3) Add the url to your `urls.py` *(if you want to use the same view for all forms submission)*
  ```py
      path("dgpf/", include("django_general_purpose_forms.urls"),),
  ```
3) Configure your forms *(see below)*
4) That's all folks!

----

## Config

> *See [example](#example) below for a full example.*

DGPF is designed to be as simple as possible to implement, but also to be as flexible as possible, so you can use it in many different ways. It will handle a few things automatically for you:
- you must inherit from `django_general_purpose_forms.forms.AbstractGeneralPurposeForm`, which will handle the genericforeignkey part of the form for you (retrieve the object)
- when the form is submitted, the generic view in `django_general_purpose_forms.views.HandleFormView` will retrieve the form class from the `DJANGO_GENERAL_PURPOSE_FORMS_CONFIG` setting, and populate the form from the request data.
  - It will then redirect to the success url defined in the form config.

<center><img src="schema.png" /></center>

### Configure your forms in `settings.py`

You need to define an identifier, a form path and a success url name for each form you want to use, this will be used to retrieve the form class from its identifier in DGPF `HandleFormView`, and to redirect to the success url after the form is submitted.

> *The key/identifier needs to be url-friendly, as it will be passed in the url when the form is submitted.*

```py
DJANGO_GENERAL_PURPOSE_FORMS_CONFIG = {
    "key": {
        "form_path": "path.to.FormClass",
        "success_url": "name_of_the_url:to_redirect_to",
        "template_name": "my_super_template.html",
    },
}
```

> *The view will try to call your success url with the `pk` of the object as a keyword argument (`reverse(success_url, kwargs={"pk": self.object.pk})`). If it fails, it will call it without any arguments (`reverse(success_url)`).*
>
> *If it fails again, it will try to return the url using success_url as a method of the object by using `getattr(obj, succss_url)()`. If that fails, it will try to return the url using success_url as a property of the object by using `getattr(obj, succss_url)` (without the parenthesis).*
>
> You can omit the `template_name` key if you want to use the default template (`django_general_purpose_forms/form.html`). If you specify a `template_name` key, it will search inside a `django_general_purpose_forms/` directory (in your project) for a template with that name.

### Update your `models.py`

In order to use django-general-purpose-forms, you'll need to add a `get_dgpf_form` method to your model, which will return an instance of the form class you defined in your settings.

```py
# add this vvvv
from .forms import MyForm
# add this ^^^

# [...]

class MyModel(models.Model):
    # [...]

    # add this vvvv
    def get_dgpf_form(self):
        return MyForm(instance=self)  # <-- instance here is really important
    # add this ^^^
```

### Create your form in `forms.py`

You can define as much fields as you want here.

The `save` method will be called when the form is valid, you can use it to send an email, save data in the database, etc.

You can also define a `form_invalid` method and handle invalid forms yourself (the default behavior is to go back to the page that sent the form, and display the errors).

> If you want to send an email, you can use the included `send_dgpf_form_by_email` method, which needs a few more vars defined in your form class.

> You can also save the object in your database using the included `save_dgpf_form` method.

```py
from django_general_purpose_forms.forms import AbstractGeneralPurposeForm

class MyForm(AbstractGeneralPurposeForm):
    form_name = "key"
    # ^^^ this is the name of your form, it's used to retrieve the form from the settings dict (in the submit view)
    first_name = forms.CharField(max_length=100)
    # [...]
    message = forms.CharField(widget=forms.Textarea)


    def save(self, request):  # request is passed by the view if you want to use the message framework
         # The form is valid, this method is called, do what you want here!
        ...
```

### Display your form in a template

If you have your object available in your template, you can simply use its `get_dgpf_form` method to get a form instance, and display it:

```django
{{ my_object.get_dgpf_form.as_p }}
```

The `form_name` attribute is also used here; it's added in the url of the form (using `action=""`), and it's used in DGPF `HandleFormView` to retrieve the form from the settings dict:

```django
<form method="post" action="{% url 'django_general_purpose_forms:handle_form_submission' form_name=my_object.get_dgpf_form.form_name %}">
```

### Customize template used for displaying errors

The template used to display errors is located in `templates/django_general_purpose_forms/form.html`. It shows the current form, with the errors, and that's it (in fact it does not even include a `<html>` tag).

You can (must?) override it in your project and customize it (add your header/footer/custom css, etc.).


## Example

Here's what a real-world implementation would look like in your project:

> **`myproject/settings.py`**

```py
DJANGO_GENERAL_PURPOSE_FORMS_CONFIG = {
    "activity": {
        "form_path": "activity.forms.ActivityContactForm",
        "success_url": "catalog:activity_detail",
    },
}
```

> **`myproject/activity/models.py`**

```py
from .forms import ActivityContactForm

class Activity(models.Model):
    name = models.CharField(
        verbose_name="Name",
        max_length=255,
    )
    # [...]

    def get_dgpf_form(self):
        return ActivityContactForm(instance=self)
```

> **`myproject/activity/forms.py`**

```py
from django_general_purpose_forms.forms import AbstractGeneralPurposeForm

class ActivityContactForm(AbstractGeneralPurposeForm):
    form_name = "activity"
    #            ^^^^^^^^ same key than in DJANGO_GENERAL_PURPOSE_FORMS_CONFIG

    # form fields:
    name = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)

    # methods related to send_dgpf_form_by_email
    def get_email_address(self):
        return [self.object.owner.email]

    def get_subject(self):
        return f"You have received an e-mail about {self.object.name}"

    def get_from_email(self):
        return settings.DEFAULT_FROM_EMAIL

    def get_txt_message(self):
        return f"From: {self.cleaned_data["name"]}\nMessage:\n{self.cleaned_data["message"]}"

    def get_html_message(self):
        return f"<pre>{self.get_txt_message()}</pre>"

    # what to do when the form is valid
    def save(self, request):
        self.send_dgpf_form_by_email()  # this method use get_email_address... get_html_message
        self.save_dgpf_form()  # this one only use get_txt_message
        messages.add_message(request, messages.INFO, "Thank you!")
```

> **`myproject/activity/templates/activity/my_model_detail.html`**

```django
{# ... page content #}

{% for message in messages %}
  <p>{{ message }}</p>
{% endfor %}

{% with object.get_dgpf_form as dgpf_form %}
  <form method="post" action="{% url 'django_general_purpose_forms:handle_form_submission' form_name=dgpf_form.form_name %}">
    {{ dgpf_form.as_p }}
    {% csrf_token %}
    <button type="submit">{% translate "Send" %}</button>
  </form>
{% endwith %}

{# page content ... #}
```

This is a simple “tunnel” implementation that redirects the visitor to a new view when the form is submitted.

You **can** define a new View or a new Mixin attached to a new url sitting in your app (`activity/views.py` & `activity/urls.py`) if you really need to implement this form in a different way.

In order to do this, all you have to do is write your view (take inspiration from `django_general_purpose_forms.views.HandleFormView`), add a new url pointing to this view in your `urls.py`, and replace the `{% url %}` tag in your template with this new url.
