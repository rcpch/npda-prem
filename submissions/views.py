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



def save_response(request ,submission):
    for field in SIMPLE_FIELDS:
        if field in request.POST:
            setattr(submission, field, request.POST[field])

    for field in JSON_FIELDS:
        if field in request.POST:
            setattr(submission, field, [v for v in request.POST.getlist(field) if v])

    submission.save()


def _get_saved_answer(submission, question_id):
    """Return the saved scalar answer for routing purposes, or None."""
    if submission is None:
        return None
    val = getattr(submission, question_id, None)
    # Multi-select JSONFields return lists; they are never routing answers.
    if isinstance(val, list):
        return None
    return val if val else None


def _next_step(sections, role, section_slug, question_id, submission=None):
    """
    Determine the next (section_slug, question_id) from the current position,
    using the submission's saved answer to resolve any routing.
    Returns (None, None) if the current question is the last in the survey.
    """
    current_section = next((s for s in sections if s["slug"] == section_slug), None)
    if current_section is None:
        return None, None

    role_qs = [q for q in current_section["questions"] if role in q.get("roles", [])]
    ix = next((i for i, q in enumerate(role_qs) if q["id"] == question_id), None)
    if ix is None:
        return None, None

    current_q = role_qs[ix]
    next_q_id = None
    next_s_slug = section_slug

    # 1. Routing via next_question map (uses saved answer if available)
    if "next_question" in current_q:
        opts = current_q["next_question"]
        answer = _get_saved_answer(submission, question_id)
        next_q_id = opts.get(answer) if (answer is not None and answer in opts) else opts.get("_")

    # 2. Sequential: next question in the same section
    if not next_q_id and ix + 1 < len(role_qs):
        next_q_id = role_qs[ix + 1]["id"]

    # 3. First question of the next section
    if not next_q_id:
        s_ix = next((i for i, s in enumerate(sections) if s["slug"] == section_slug), None)
        if s_ix is not None:
            for s in sections[s_ix + 1:]:
                rqs = [q for q in s["questions"] if role in q.get("roles", [])]
                if rqs:
                    next_s_slug = s["slug"]
                    next_q_id = rqs[0]["id"]
                    break

    if not next_q_id:
        return None, None  # end of survey

    # If routing jumped to a question outside the current section, find its section.
    if next_q_id not in {q["id"] for q in role_qs}:
        for s in sections:
            if any(q["id"] == next_q_id for q in s["questions"] if role in q.get("roles", [])):
                next_s_slug = s["slug"]
                break

    return next_s_slug, next_q_id


def traverse_survey(sections, role, target_section_slug, target_question_id, submission=None):
    """
    Walk from the first question using saved answers to follow routing decisions.
    Returns (position, prev_section_slug, prev_question_id), position is 1-based.
    Returns None if the target question is unreachable from the start.
    """
    current_s_slug = None
    current_q_id = None
    for s in sections:
        rqs = [q for q in s["questions"] if role in q.get("roles", [])]
        if rqs:
            current_s_slug = s["slug"]
            current_q_id = rqs[0]["id"]
            break

    if current_q_id is None:
        return None

    position = 0
    prev_s_slug = None
    prev_q_id = None
    visited = set()

    while current_q_id is not None:
        key = (current_s_slug, current_q_id)
        if key in visited:
            return None  # cycle guard
        visited.add(key)
        position += 1

        if current_s_slug == target_section_slug and current_q_id == target_question_id:
            return (position, prev_s_slug, prev_q_id)

        prev_s_slug = current_s_slug
        prev_q_id = current_q_id
        current_s_slug, current_q_id = _next_step(
            sections, role, current_s_slug, current_q_id, submission
        )

    return None  # target not found


def count_remaining_questions(sections, role, current_section_slug, current_question_id):
    """
    Count questions from the current (inclusive) to the end, following default
    routing (no saved answers — uses sequential or '_' fallbacks only).
    """
    count = 0
    s_slug = current_section_slug
    q_id = current_question_id
    visited = set()

    while q_id is not None:
        key = (s_slug, q_id)
        if key in visited:
            break
        visited.add(key)
        count += 1
        s_slug, q_id = _next_step(sections, role, s_slug, q_id, submission=None)

    return count



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