import csv

from django.contrib import admin
from django.db.models import Count, Q
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path

from .clinics import CLINICS
from .models import Submission, SubmissionPeriod

# Build a lookup: pz_code → first familiar clinic name
_PZ_NAME = {}
for _c in CLINICS:
    _PZ_NAME.setdefault(_c["pz_code"], _c["name"])


@admin.action(description="Export selected submissions as CSV")
def export_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="submissions.csv"'

    field_names = [
        "id",
        "role",
        "language",
        "submitted",
        "pz_code",
        "q4_gender",
        "q5_relationship",
        "q6_diabetes_type",
        "q7_age_at_diagnosis",
        "q8_ethnicity",
        "q9_education_stage",
        "q9_education_stage_other",
        "q10_school_type",
        "q11_home_education_reason",
        "q12_free_school_meals",
        "q13_healthcare_plan",
        "q14_plan_coverage",
        "q15_school_contact",
        "q16_insulin_or_monitor",
        "q17_insulin_method",
        "q18_glucose_monitoring",
        "q19_remote_monitoring",
        "q20_contact_school",
        "q21_smartphone_use",
        "q22_private_room",
        "q23_classroom_management",
        "q24_trained_staff",
        "q25_carb_counting",
        "q26_missed_lessons",
        "q27_absences_authorised",
        "q28_attendance_impacted",
        "q29_days_off",
        "q30_moved_schools",
        "q31_excluded_activities",
        "q31_excluded_activities_other",
        "q32_performance_impact",
        "q33_teacher_understanding",
        "q34_reasonable_adjustments",
        "q35_felt_left_out",
        "q36_lost_income",
        "q37_anxiety_frequency",
        "q38_school_support",
        "q39_team_support",
        "q40_worked_well",
        "q41_not_worked_well",
        "q42_improvements",
        "created_at",
        "updated_at",
    ]

    writer = csv.writer(response)
    writer.writerow(field_names)

    for obj in queryset.order_by("id"):
        row = []
        for field in field_names:
            value = getattr(obj, field)
            if isinstance(value, list):
                value = ", ".join(value) if value else ""
            row.append(value)
        writer.writerow(row)

    return response


@admin.register(SubmissionPeriod)
class SubmissionPeriodAdmin(admin.ModelAdmin):
    list_display = ("year", "is_open")
    list_editable = ("is_open",)
    ordering = ("-year",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "role", "language", "submitted", "pz_code", "q38_school_support", "created_at")
    list_filter = ("role", "submitted", "language", "pz_code")
    readonly_fields = ("created_at", "updated_at")
    actions = [export_as_csv]

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path(
                "by-pz-code/",
                self.admin_site.admin_view(self.by_pz_code_view),
                name="submissions_by_pz_code",
            ),
            path(
                "by-pz-code/export.csv",
                self.admin_site.admin_view(self.by_pz_code_csv),
                name="submissions_by_pz_code_csv",
            ),
        ]
        return custom + urls

    def by_pz_code_view(self, request):
        rows = (
            Submission.objects
            .exclude(pz_code="")
            .values("pz_code")
            .annotate(
                complete=Count("id", filter=Q(submitted=True)),
                partial=Count("id", filter=Q(submitted=False)),
                total=Count("id"),
            )
            .order_by("pz_code")
        )

        data = []
        for row in rows:
            row["clinic_name"] = _PZ_NAME.get(row["pz_code"], "Unknown")
            data.append(row)

        totals = {
            "complete": sum(r["complete"] for r in data),
            "partial": sum(r["partial"] for r in data),
            "total": sum(r["total"] for r in data),
        }

        context = {
            **self.admin_site.each_context(request),
            "title": "Submissions by PZ code",
            "rows": data,
            "totals": totals,
        }
        return TemplateResponse(
            request, "admin/submissions_by_pz_code.html", context
        )

    def by_pz_code_csv(self, request):
        rows = (
            Submission.objects
            .exclude(pz_code="")
            .values("pz_code")
            .annotate(
                complete=Count("id", filter=Q(submitted=True)),
                partial=Count("id", filter=Q(submitted=False)),
                total=Count("id"),
            )
            .order_by("pz_code")
        )

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="submissions_by_pz_code.csv"'

        writer = csv.writer(response)
        writer.writerow(["PZ Code", "Clinic Name", "Partial", "Complete", "Total"])

        for row in rows:
            writer.writerow([
                row["pz_code"],
                _PZ_NAME.get(row["pz_code"], "Unknown"),
                row["partial"],
                row["complete"],
                row["total"],
            ])

        return response
