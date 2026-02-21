import json

from django.http import Http404, HttpResponse
from django.core.exceptions import SuspiciousOperation
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _
from django.conf import settings

from .clinics import (
    get_all_clinics_sorted,
    get_clinics_for_region,
    REGION_SLUG_MAP,
    get_current_clinic_display_name,
    get_all_clinic_display_names,
    get_pz_code_by_display_name
)
from .models import Submission, SubmissionPeriod, GENDER_CHOICES, DIABETES_TYPE_CHOICES
from .section_navigation import _next_step, traverse_survey, count_remaining_questions, find_resume_question
from .sections import build_sections
from .turnstile import validate_turnstile


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
# Pages
# ---------------------------------------------------------------------------

def get_open_submission_period():
    """Return the latest SubmissionPeriod if it is open, otherwise None."""
    period = SubmissionPeriod.objects.order_by("-year").first()
    if period and period.is_open:
        return period
    return None


def landing(request):
    if get_open_submission_period() is None:
        return render(request, "submissions/submissions_closed.html")

    if request.session.get("submission_id"):
        if Submission.objects.filter(pk=request.session["submission_id"], submitted=False).exists():
            return redirect(reverse("resume_or_new"))

    ctx = {
        # Link is modified using JS on the frontend depending on language selected
        "next_url": reverse("front_matter", kwargs={"lang": "en"}),
    }

    if request.session.get("tablet_mode") and "pz_code" in request.session:
        # TODO MRB: need to show front matter then jump straight to role form
        ctx["next_url"] = reverse("role_form", kwargs={"lang": "en"})

    return render(request, "submissions/landing.html", ctx)


def front_matter(request, lang):
    ctx = {
        "lang": lang,
        "next_url": reverse("clinic_or_region", kwargs={"lang": lang}),
    }

    return render(request, "submissions/front_matter.html", ctx)


def get_current_clinic_name_with_region(request, clinics):
    clinics = get_all_clinics_sorted()

    if "pz_code" in request.session:
        for clinic in clinics:
            if clinic["pz_code"] == request.session["pz_code"]:
                return f"{clinic['name']} - {clinic['region']}"


def get_clinic_json(pz_code):
    clinic_display_names = get_all_clinic_display_names()
    current_clinic_display_name = get_current_clinic_display_name(pz_code)
    
    clinic_json = json.dumps({
        "clinic_display_names": clinic_display_names,
        "current_clinic_display_name": current_clinic_display_name
    })

    return clinic_json


def clinic_or_region(request, lang):
    """Step 1: select the region (or 'unsure')."""
    if request.method == "POST":
        clinic_value = request.POST.get("clinic", "")
        region = request.POST.get("region", "")

        pz_code = get_pz_code_by_display_name(clinic_value)

        if pz_code:
            request.session["pz_code"] = pz_code
            return redirect(reverse("role_form", kwargs={"lang": lang}))
        else:
            return redirect(reverse("clinic_in_region", kwargs={"lang": lang, "region": region}))

    clinics = get_all_clinics_sorted()
    
    regions = sorted(set(clinic["region"] for clinic in clinics))
    regions_with_slugs = [(REGION_SLUG_MAP[r], r) for r in regions]

    return render(request, "submissions/clinic_or_region.html", {
        "lang": lang,
        "region": None, # always select again
        "regions_with_slugs": regions_with_slugs,
        "clinic_json": get_clinic_json(request.session.get("pz_code")),
        "prev_url": reverse("front_matter", kwargs={"lang": lang}),
    })


def clinic_in_region(request, lang, region):
    """Step 2: select the clinic from the chosen region (or all if unsure)."""
    if request.method == "POST":
        pz_code = request.POST.get("pz_code", "")
        request.session["pz_code"] = pz_code
        return redirect(reverse("role_form", kwargs={"lang": lang}))

    if region == "all":
        clinics = get_all_clinics_sorted()
    else:
        clinics = get_clinics_for_region(region)

    return render(request, "submissions/clinic_in_region.html", {
        "lang": lang,
        "region": region,
        "clinics": clinics,
        "pz_code": request.session.get("pz_code", ""),
        "clinic_json": get_clinic_json(request.session.get("pz_code")),
    })


def role_form(request, lang):
    # TODO MRB: needs to remember your selector

    prev_url = reverse("clinic_or_region", kwargs={"lang": lang})

    if request.session.get("tablet_mode") and "pz_code" in request.session:
        prev_url = reverse("landing")

    ctx = {
        "lang": lang,
        "current_clinic_display_name": get_current_clinic_display_name(request.session.get("pz_code")),
        "prev_url": prev_url
    }

    return render(request, "submissions/role_form.html", ctx)


def confirmation(request, lang):
    return render(request, "submissions/confirmation.html", {"lang": lang})


def resume_or_new(request):
    submission_id = request.session.get("submission_id")
    if not submission_id:
        return redirect(reverse("landing"))

    try:
        submission = Submission.objects.get(pk=submission_id, submitted=False)
    except Submission.DoesNotExist:
        if "submission_id" in request.session:
            del request.session["submission_id"]
        return redirect(reverse("landing"))

    if request.POST:
        action = request.POST.get("action")

        if action == "continue":
            sections = [s for s in build_sections() if submission.role in s.get("roles", [])]
            result = find_resume_question(sections, submission.role, submission)
            if result:
                s_slug, q_id = result
                return redirect(reverse("question", kwargs={
                    "lang": submission.language,
                    "role": submission.role,
                    "section": s_slug,
                    "question": q_id,
                }))

        elif action == "start_new":
            reset_session(request)

        return redirect(reverse("landing"))

    return render(request, "submissions/resume_or_new.html", {})



def save_response(request ,submission):
    for field in SIMPLE_FIELDS:
        if field in request.POST:
            setattr(submission, field, request.POST[field])

    for field in JSON_FIELDS:
        if field in request.POST:
            setattr(submission, field, [v for v in request.POST.getlist(field) if v])

    submission.save()



def question(request, lang, role, section, question):
    if request.POST and not request.session.get("not_a_bot"):
        token = request.POST.get("cf-turnstile-response", "")

        # throws on error
        validate_turnstile(token, remoteip=request.META.get("REMOTE_ADDR"))
        request.session["not_a_bot"] = True

    sections = [s for s in build_sections() if role in s.get("roles", [])]

    section_data = next((s for s in sections if s["slug"] == section), None)
    if section_data is None:
        raise Http404

    # Filter questions by role within this section
    role_questions = [q for q in section_data["questions"] if role in q.get("roles", [])]

    question_data = None
    question_ix = 0

    for ix, q in enumerate(role_questions):
        if q["id"] == question:
            question_data = q
            question_ix = ix
            break

    if question_data is None:
        raise Http404

    question_data["title"] = question_data["title"][role]

    submission = None
    submission_id = request.session.get("submission_id")

    if submission_id:
        try:
            submission = Submission.objects.get(
                pk=submission_id, submitted=False
            )
        except Submission.DoesNotExist:
            pass
    
    if request.POST:
        if submission is None:
            submission = Submission.objects.create(
                role=role,
                language=lang,
                pz_code=request.session.get("pz_code", ""),
                submission_period=get_open_submission_period(),
            )
            request.session["submission_id"] = submission.pk
        
        save_response(request, submission)

        next_section_slug, next_question_id = _next_step(
            sections, role, section_data["slug"], question_data["id"], submission
        )

        if next_question_id is None:
            submission.submitted = True
            submission.save()
            del request.session["submission_id"]
            return redirect(reverse("confirmation", kwargs={"lang": lang}))

        return redirect(reverse("question", kwargs={
            "lang": lang,
            "role": role,
            "section": next_section_slug,
            "question": next_question_id,
        }))
    
    result = traverse_survey(sections, role, section_data["slug"], question_data["id"], submission)
    if result is None:
        question_number = 1
        prev_url = reverse("role_form", kwargs={"lang": lang})
    else:
        question_number, prev_s_slug, prev_q_id = result
        if prev_q_id is None:
            prev_url = reverse("role_form", kwargs={"lang": lang})
        else:
            prev_url = reverse("question", kwargs={
                "lang": lang,
                "role": role,
                "section": prev_s_slug,
                "question": prev_q_id,
            })

    question_total = (question_number - 1) + count_remaining_questions(
        sections, role, section_data["slug"], question_data["id"]
    )

    ctx = {
        "question": question_data,
        "field_value": getattr(submission, question_data["id"]) if submission else None,
        "prev_url": prev_url,
        "lang": lang,
        "role": role,
        "current_clinic_display_name": get_current_clinic_display_name(request.session.get("pz_code")),
        "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
        "not_a_bot": request.session.get("not_a_bot", False),
        "question_number": question_number,
        "question_total": question_total,
    }

    if question_ix == 0:
        ctx["section_title"] = section_data["title"]
        ctx["section_introduction"] = section_data.get("introduction")

    ctx["submission"] = submission

    return render(request, f"submissions/question.html", ctx)


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

def reset_session(request):
    keys_to_clear = ["submission_id"]

    if "tablet_mode" not in request.session:
        keys_to_clear.append("pz_code")

    for key in keys_to_clear:
        if key in request.session:
            del request.session[key]

@require_POST
def start_again(request):
    reset_session(request)

    return redirect(reverse("landing"))


def tablet_mode(request):
    preselected_pz_code = None

    for clinic in get_all_clinics_sorted():
        if clinic["pz_code"] == request.GET.get("pz_code", ""):
            preselected_pz_code = clinic["pz_code"]
            break

    if request.POST:
        action = request.POST.get("action")

        match action:
            case "enable_tablet_mode":
                clinic_value = request.POST.get("clinic", "")
                pz_code = get_pz_code_by_display_name(clinic_value)

                if not pz_code:
                    raise SuspiciousOperation(f"Unknown clinic {clinic_value} selected for tablet mode")

                request.session["pz_code"] = pz_code
                request.session["tablet_mode"] = True
            case "disable_tablet_mode" if "tablet_mode" in request.session:
                if "pz_code" in request.session:
                    del request.session["pz_code"]
                
                if "tablet_mode" in request.session:
                    del request.session["tablet_mode"]
        
        reset_session(request)
        return redirect(reverse("landing"))

    clinics = get_all_clinics_sorted()

    ctx = {
        "clinic_json": get_clinic_json(preselected_pz_code or request.session.get("pz_code")),
        "tablet_mode_enabled": "tablet_mode" in request.session,
    }

    return render(request, "submissions/tablet-mode.html", ctx)