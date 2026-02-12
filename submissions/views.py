from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .clinics import get_all_clinics, get_clinics_for_region
from .models import Submission


# Simple fields that map directly from POST key to model field (CharField / TextField).
SIMPLE_FIELDS = [
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
# Section definitions
# ---------------------------------------------------------------------------

PARENT_SECTIONS = [
    {
        "slug": "demographics",
        "title": "Demographics",
        "template": "submissions/_parent_demographics.html",
    },
    {
        "slug": "healthcare-plans",
        "title": "School Health Care Plans",
        "template": "submissions/_parent_healthcare_plans.html",
    },
    {
        "slug": "managing-diabetes",
        "title": "Managing Diabetes",
        "template": "submissions/_parent_managing_diabetes.html",
    },
    {
        "slug": "education-impact",
        "title": "Impact on Education",
        "template": "submissions/_shared_education_impact.html",
    },
    {
        "slug": "wellbeing",
        "title": "Social and Emotional Impact",
        "template": "submissions/_shared_wellbeing.html",
    },
]

CHILD_SECTIONS = [
    {
        "slug": "demographics",
        "title": "Demographics",
        "template": "submissions/_child_demographics.html",
    },
    {
        "slug": "managing-diabetes",
        "title": "Managing Diabetes",
        "template": "submissions/_child_managing_diabetes.html",
    },
    {
        "slug": "education-impact",
        "title": "Impact on Education",
        "template": "submissions/_shared_education_impact.html",
    },
    {
        "slug": "wellbeing",
        "title": "Social and Emotional Impact",
        "template": "submissions/_shared_wellbeing.html",
    },
]


def _section_context(sections, section_slug, form_url_name, lang):
    """Build template context for the current section."""
    slugs = [s["slug"] for s in sections]
    if section_slug not in slugs:
        raise Http404
    idx = slugs.index(section_slug)

    prev_url = (
        reverse(form_url_name, kwargs={"lang": lang, "section": slugs[idx - 1]})
        if idx > 0
        else None
    )
    next_url = (
        reverse(form_url_name, kwargs={"lang": lang, "section": slugs[idx + 1]})
        if idx < len(sections) - 1
        else None
    )

    return {
        "sections": sections,
        "current_index": idx,
        "current_display": idx + 1,
        "total_sections": len(sections),
        "section_template": sections[idx]["template"],
        "prev_url": prev_url,
        "next_url": next_url,
        "is_last_section": idx == len(sections) - 1,
        "lang": lang,
    }


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def landing(request):
    return render(request, "submissions/landing.html")


def clinic_or_region_form(request, lang):
    """Step 1: select the region (or 'unsure')."""
    if request.method == "POST":
        region = request.POST.get("q1_region", "")
        request.session["q1_region"] = region
        return redirect(reverse("clinic_form", kwargs={"lang": lang}))

    return render(request, "submissions/clinic_or_region.html", {
        "lang": lang,
        "q1_region": request.session.get("q1_region", ""),
        "clinics": get_all_clinics(),
    })


def clinic_form(request, lang):
    """Step 2: select the clinic from the chosen region (or all if unsure)."""
    region = request.session.get("q1_region", "")

    if request.method == "POST":
        pz_code = request.POST.get("pz_code", "")
        request.session["pz_code"] = pz_code
        return redirect(reverse("role_form", kwargs={"lang": lang}))

    if region == "unsure" or not region:
        clinics = get_all_clinics()
    else:
        clinics = get_clinics_for_region(region)

    return render(request, "submissions/clinic_select.html", {
        "lang": lang,
        "region": region,
        "clinics": clinics,
        "selected_pz_code": request.session.get("pz_code", ""),
    })


def role_form(request, lang):
    return render(request, "submissions/form.html", {"lang": lang})


def confirmation(request, lang):
    return render(request, "submissions/confirmation.html", {"lang": lang})


# ---------------------------------------------------------------------------
# Parent form
# ---------------------------------------------------------------------------

def parent_form(request, lang, section=None):
    if section is None:
        return redirect(
            reverse("parent_form_section", kwargs={"lang": lang, "section": PARENT_SECTIONS[0]["slug"]})
        )

    submission = None
    submission_id = request.session.get("submission_id")

    if submission_id:
        try:
            submission = Submission.objects.get(
                pk=submission_id, role="parent", submitted=False
            )
        except Submission.DoesNotExist:
            del request.session["submission_id"]

    ctx = _section_context(PARENT_SECTIONS, section, "parent_form_section", lang)
    ctx["submission"] = submission
    return render(request, "submissions/parent_form.html", ctx)


@require_POST
def parent_autosave(request, lang):
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
            language=lang,
            q1_region=request.session.get("q1_region", ""),
            pz_code=request.session.get("pz_code", ""),
        )
        request.session["submission_id"] = submission.pk

    _save_fields(submission, request)
    return HttpResponse(status=204)


@require_POST
def parent_submit(request, lang):
    submission_id = request.session.get("submission_id")

    if not submission_id:
        return redirect(reverse("parent_form", kwargs={"lang": lang}))

    submission = get_object_or_404(Submission, pk=submission_id, submitted=False)
    submission.submitted = True
    submission.save()

    del request.session["submission_id"]
    return redirect(reverse("confirmation", kwargs={"lang": lang}))


# ---------------------------------------------------------------------------
# Child / young person form
# ---------------------------------------------------------------------------

def child_form(request, lang, section=None):
    if section is None:
        return redirect(
            reverse("child_form_section", kwargs={"lang": lang, "section": CHILD_SECTIONS[0]["slug"]})
        )

    submission = None
    submission_id = request.session.get("submission_id")

    if submission_id:
        try:
            submission = Submission.objects.get(
                pk=submission_id, role="cyp", submitted=False
            )
        except Submission.DoesNotExist:
            del request.session["submission_id"]

    ctx = _section_context(CHILD_SECTIONS, section, "child_form_section", lang)
    ctx["submission"] = submission
    return render(request, "submissions/child_form.html", ctx)


@require_POST
def child_autosave(request, lang):
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
            language=lang,
            q1_region=request.session.get("q1_region", ""),
            pz_code=request.session.get("pz_code", ""),
        )
        request.session["submission_id"] = submission.pk

    _save_fields(submission, request)
    return HttpResponse(status=204)


@require_POST
def child_submit(request, lang):
    submission_id = request.session.get("submission_id")

    if not submission_id:
        return redirect(reverse("child_form", kwargs={"lang": lang}))

    submission = get_object_or_404(Submission, pk=submission_id, submitted=False)
    submission.submitted = True
    submission.save()

    del request.session["submission_id"]
    return redirect(reverse("confirmation", kwargs={"lang": lang}))


# ---------------------------------------------------------------------------
# Start again
# ---------------------------------------------------------------------------

def start_again(request, lang):
    submission_id = request.session.get("submission_id")
    if submission_id:
        Submission.objects.filter(pk=submission_id, submitted=False).delete()
        del request.session["submission_id"]

    return redirect(reverse("landing"))
