import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .clinics import get_all_clinics, get_clinics_for_region, REGION_SLUG_MAP
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


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def landing(request):
    return render(request, "submissions/landing.html")


def clinic_or_region(request, lang):
    """Step 1: select the region (or 'unsure')."""
    if request.method == "POST":
        clinic_value = request.POST.get("clinic", "")
        region = request.POST.get("region", "")

        if clinic_value:
            for clinic in get_all_clinics():
                if clinic_value == f"{clinic['name']} - {clinic['region']}":
                    request.session["pz_code"] = clinic["pz_code"]
            
            if "pz_code" in request.session:
                return redirect(reverse("role_form", kwargs={"lang": lang}))
        else:
            return redirect(reverse("clinic_in_region", kwargs={"lang": lang, "region": region}))

    clinics = get_all_clinics()
    
    regions = sorted(set(clinic["region"] for clinic in clinics))
    regions_with_slugs = [(REGION_SLUG_MAP[r], r) for r in regions]

    clinic_names_with_regions = [f"{clinic['name']} - {clinic['region']}" for clinic in get_all_clinics()]

    selected_clinic_name_with_region = None
    if "pz_code" in request.session:
        for clinic in clinics:
            if clinic["pz_code"] == request.session["pz_code"]:
                selected_clinic_name_with_region = f"{clinic['name']} - {clinic['region']}"
                break
    
    clinic_json = json.dumps({
        "clinic_names_with_regions": clinic_names_with_regions,
        "selected_clinic_name_with_region": selected_clinic_name_with_region
    })

    return render(request, "submissions/clinic_or_region.html", {
        "lang": lang,
        "region": None, # always select again
        "regions_with_slugs": regions_with_slugs,
        "clinic_json": clinic_json
    })


def clinic_in_region(request, lang, region):
    """Step 2: select the clinic from the chosen region (or all if unsure)."""
    if request.method == "POST":
        pz_code = request.POST.get("pz_code", "")
        request.session["pz_code"] = pz_code
        return redirect(reverse("role_form", kwargs={"lang": lang}))

    if region == "all":
        clinics = get_all_clinics()
    else:
        clinics = get_clinics_for_region(region)

    return render(request, "submissions/clinic_in_region.html", {
        "lang": lang,
        "region": region,
        "clinics": clinics,
        "pz_code": request.session.get("pz_code", ""),
    })


def role_form(request, lang):
    return render(request, "submissions/role_form.html", {"lang": lang})


def confirmation(request, lang):
    return render(request, "submissions/confirmation.html", {"lang": lang})


def get_idx_prev_next(lang, role, sections, section):
    slugs = [s["slug"] for s in sections]

    if section not in slugs:
        raise Http404
    
    idx = slugs.index(section)

    prev_url = (
        reverse("form_section", kwargs={"lang": lang, "role": role, "section": slugs[idx - 1]})
        if idx > 0
        else reverse("role_form", kwargs={"lang": lang})
    )

    next_url = (
        reverse("form_section", kwargs={"lang": lang, "role": role, "section": slugs[idx + 1]})
        if idx < len(sections) - 1
        else None
    )

    return (idx, prev_url, next_url)


def form(request, lang, role, section=None):
    form_url_name = f"{role}_section"

    sections = PARENT_SECTIONS if role == "parent" else CHILD_SECTIONS

    if section is None:
        return redirect(
            reverse("form_section", kwargs={"lang": lang, "role": role, "section": sections[0]["slug"]})
        )

    submission = None
    submission_id = request.session.get("submission_id")

    if submission_id:
        try:
            submission = Submission.objects.get(
                pk=submission_id, submitted=False
            )
        except Submission.DoesNotExist:
            del request.session["submission_id"]
            return redirect(reverse("landing"))

    (idx, prev_url, next_url) = get_idx_prev_next(lang, role, sections, section)

    ctx = {
        "sections": sections,
        "current_index": idx,
        "current_display": idx + 1,
        "total_sections": len(sections),
        "section_template": sections[idx]["template"],
        "prev_url": prev_url,
        "next_url": next_url,
        "is_last_section": idx == len(sections) - 1,
        "lang": lang,
        "role": role,
    }

    ctx["submission"] = submission

    return render(request, f"submissions/form.html", ctx)


@require_POST
def autosave(request, lang, role):
    submission_id = request.session.get("submission_id")
    submission = None

    if submission_id:
        try:
            submission = Submission.objects.get(pk=submission_id, submitted=False)
        except Submission.DoesNotExist:
            pass

    if submission is None:
        submission = Submission.objects.create(
            role=role,
            language=lang,
            pz_code=request.session.get("pz_code", ""),
        )
        request.session["submission_id"] = submission.pk

    for field in SIMPLE_FIELDS:
        if field in request.POST:
            setattr(submission, field, request.POST[field])

    for field in JSON_FIELDS:
        if field in request.POST:
            setattr(submission, field, [v for v in request.POST.getlist(field) if v])

    submission.save()

    return HttpResponse(status=204)


@require_POST
def submit(request, lang, role):
    submission_id = request.session.get("submission_id")

    if not submission_id:
        return redirect(reverse("form", kwargs={"lang": lang, "role": role}))

    submission = get_object_or_404(Submission, pk=submission_id, submitted=False)
    submission.submitted = True
    submission.save()

    del request.session["submission_id"]
    return redirect(reverse("confirmation", kwargs={"lang": lang}))


# ---------------------------------------------------------------------------
# Start again
# ---------------------------------------------------------------------------

@require_POST
def start_again(request):
    submission_id = request.session.get("submission_id")
    if submission_id:
        del request.session["submission_id"]

    return redirect(reverse("landing"))
