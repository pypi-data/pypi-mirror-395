# Django
from django.urls import path

# Project
from django_general_purpose_forms.views import HandleFormView

app_name = "django_general_purpose_forms"

urlpatterns = [
    path(
        "send/<str:form_name>/",
        HandleFormView.as_view(),
        name="handle_form_submission",
    ),
]
