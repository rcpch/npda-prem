from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Submission


def _get_lang(request):
    return request.GET.get("lang", "en")


def _lang_qs(request):
    return f"?lang={_get_lang(request)}"


# Simple fields that map directly from POST key to model field (CharField / TextField).
SIMPLE_FIELDS = [
    "q1_region",
    "q2_hospital",
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
]

# Multi-select (JSONField) fields – POST sends multiple values.
JSON_FIELDS = [
    "q17_insulin_method",
    "q18_glucose_monitoring",
    "q31_excluded_activities",
]


def _save_fields(submission, request):
    """Update a submission from POST data (autosave or final submit)."""
    for field in SIMPLE_FIELDS:
        if field in request.POST:
            setattr(submission, field, request.POST[field])

    for field in JSON_FIELDS:
        if field in request.POST:
            setattr(submission, field, [v for v in request.POST.getlist(field) if v])

    submission.save()


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def landing(request):
    return render(request, "submissions/landing.html")


def submission_form(request):
    return render(request, "submissions/form.html")


def confirmation(request):
    return render(request, "submissions/confirmation.html")


# ---------------------------------------------------------------------------
# Parent form
# ---------------------------------------------------------------------------

def parent_form(request):
    submission = None
    submission_id = request.session.get("submission_id")

    if submission_id:
        try:
            submission = Submission.objects.get(
                pk=submission_id, role="parent", submitted=False
            )
        except Submission.DoesNotExist:
            del request.session["submission_id"]

    return render(request, "submissions/parent_form.html", {"submission": submission})


@require_POST
def parent_autosave(request):
    submission_id = request.session.get("submission_id")
    submission = None

    if submission_id:
        try:
            submission = Submission.objects.get(pk=submission_id, submitted=False)
        except Submission.DoesNotExist:
            pass

    if submission is None:
        submission = Submission.objects.create(
            role="parent",
            language=_get_lang(request),
        )
        request.session["submission_id"] = submission.pk

    _save_fields(submission, request)
    return HttpResponse(status=204)


@require_POST
def parent_submit(request):
    submission_id = request.session.get("submission_id")

    if not submission_id:
        return redirect(reverse("parent_form") + _lang_qs(request))

    submission = get_object_or_404(Submission, pk=submission_id, submitted=False)
    submission.submitted = True
    submission.save()

    del request.session["submission_id"]
    return redirect(reverse("confirmation") + _lang_qs(request))


# ---------------------------------------------------------------------------
# Child / young person form
# ---------------------------------------------------------------------------

def child_form(request):
    submission = None
    submission_id = request.session.get("submission_id")

    if submission_id:
        try:
            submission = Submission.objects.get(
                pk=submission_id, role="cyp", submitted=False
            )
        except Submission.DoesNotExist:
            del request.session["submission_id"]

    return render(request, "submissions/child_form.html", {"submission": submission})


@require_POST
def child_autosave(request):
    submission_id = request.session.get("submission_id")
    submission = None

    if submission_id:
        try:
            submission = Submission.objects.get(pk=submission_id, submitted=False)
        except Submission.DoesNotExist:
            pass

    if submission is None:
        submission = Submission.objects.create(
            role="cyp",
            language=_get_lang(request),
        )
        request.session["submission_id"] = submission.pk

    _save_fields(submission, request)
    return HttpResponse(status=204)


@require_POST
def child_submit(request):
    submission_id = request.session.get("submission_id")

    if not submission_id:
        return redirect(reverse("child_form") + _lang_qs(request))

    submission = get_object_or_404(Submission, pk=submission_id, submitted=False)
    submission.submitted = True
    submission.save()

    del request.session["submission_id"]
    return redirect(reverse("confirmation") + _lang_qs(request))


# ---------------------------------------------------------------------------
# Start again
# ---------------------------------------------------------------------------

def start_again(request):
    submission_id = request.session.get("submission_id")
    if submission_id:
        Submission.objects.filter(pk=submission_id, submitted=False).delete()
        del request.session["submission_id"]

    return redirect(reverse("landing"))
