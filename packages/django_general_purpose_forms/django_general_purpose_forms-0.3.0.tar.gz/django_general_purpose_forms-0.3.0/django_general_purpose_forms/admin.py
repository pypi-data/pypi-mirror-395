# Django
from django.contrib import admin

# Local application / specific library imports
from .models import SentForm


@admin.register(SentForm)
class SentFormAdmin(admin.ModelAdmin):
    list_display = ("id", "date_sent", "content_object")
    list_display_links = ("id", "date_sent")
    list_filter = ("content_type",)
    search_fields = ("content", "content_object")
    readonly_fields = ("date_sent", "content_object", "content")
    fields = ("date_sent", "content_object", "content")
