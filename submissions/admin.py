import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Submission


@admin.action(description="Export selected submissions as CSV")
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="submissions.csv"'

    field_names = [
        "id",
        "role",
        "language",
        "submitted",
        "contact",
        "rating",
        "hospital",
        "child_age",
        "comments",
        "created_at",
        "updated_at",
    ]

    writer = csv.writer(response)
    writer.writerow(field_names)

    for obj in queryset.order_by("id"):
        row = []
        for field in field_names:
            value = getattr(obj, field)
            if field == "contact":
                value = ", ".join(value) if value else ""
            row.append(value)
        writer.writerow(row)

    return response


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "language", "submitted", "rating", "hospital", "created_at")
    list_filter = ("role", "submitted", "language")
    readonly_fields = ("created_at", "updated_at")
    actions = [export_as_csv]
