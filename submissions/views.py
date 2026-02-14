import json

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext as _

from .clinics import get_all_clinics, get_clinics_for_region, REGION_SLUG_MAP
from .models import Submission, GENDER_CHOICES, DIABETES_TYPE_CHOICES
from .sections import build_sections


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

def landing(request):
    return render(request, "submissions/landing.html")


def get_current_clinic_name_with_region(request, clinics):
    clinics = get_all_clinics()

    if "pz_code" in request.session:
        for clinic in clinics:
            if clinic["pz_code"] == request.session["pz_code"]:
                return f"{clinic['name']} - {clinic['region']}"


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

    selected_clinic_name_with_region = get_current_clinic_name_with_region(request, clinics)
    
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
    # TODO MRB: needs to remember your selector
    ctx = {
        "lang": lang,
        "current_clinic_name_with_region": get_current_clinic_name_with_region(request, get_all_clinics()),
    }

    return render(request, "submissions/role_form.html", ctx)


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


def save_response(request ,submission):
    for field in SIMPLE_FIELDS:
        if field in request.POST:
            setattr(submission, field, request.POST[field])

    for field in JSON_FIELDS:
        if field in request.POST:
            setattr(submission, field, [v for v in request.POST.getlist(field) if v])

    submission.save()


def get_prev_url(request, lang, role, section_data_slug, question_data_id):
    # Prune history
    history_before = request.session.get("history", [])
    history_after = []

    for (section_slug, question_id) in history_before:
        if section_slug == section_data_slug and question_id == question_data_id:
            break
        
        history_after.append((section_slug, question_id))
    
    request.session["history"] = history_after

    if not request.session.get("history"):
        prev_url = reverse("role_form", kwargs={"lang": lang}) # default to role form if no previous question
    else:
        prev_url = reverse("question", kwargs={
            "lang": lang,
            "role": role,
            "section": request.session["history"][-1][0],
            "question": request.session["history"][-1][1],
        })

    return prev_url


def section(request, lang, role, section):
    sections = [s for s in build_sections() if role in s.get("roles", [])]

    section_data = None
    section_ix = 0

    for ix, s in enumerate(sections):
        if s["slug"] == section:
            section_data = s
            section_ix = ix
            break

    if section_data is None:
        raise Http404

    prev_url = get_prev_url(request, lang, role, section_data["slug"], question_data_id=None)

    role_questions = [q for q in section_data["questions"] if role in q.get("roles", [])]

    next_url = reverse("question", kwargs={
        "lang": lang,
        "role": role,
        "section": section_data["slug"],
        "question": role_questions[0]["id"]
    })

    ctx = {
        "section": section_data,
        "prev_url": prev_url,
        "next_url": next_url,
        "lang": lang,
        "role": role,
        "current_clinic_name_with_region": get_current_clinic_name_with_region(request, get_all_clinics()),
    }

    return render(request, f"submissions/section.html", ctx)



def question(request, lang, role, section, question):
    sections = [s for s in build_sections() if role in s.get("roles", [])]

    section_data = None
    section_ix = 0

    for ix, s in enumerate(sections):
        if s["slug"] == section:
            section_data = s
            section_ix = ix
            break

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
            )
            request.session["submission_id"] = submission.pk
        
        save_response(request, submission)

        # TODO MRB: my kingdom for a dataclass!
        history = request.session.get("history", [])
        history.append((section_data["slug"], question_data["id"]))
        request.session["history"] = history

        next_section_id = section_data["slug"]
        next_question_id = None

        if "next_question" in question_data:
            next_question_options = question_data["next_question"]
            value = request.POST.get(question_data["id"], "")

            if value in next_question_options:
                next_question_id = next_question_options[value]
            else:
                next_question_id = next_question_options["_"]
        
        if not next_question_id:
            if question_ix < len(role_questions) - 1:
                next_question_id = role_questions[question_ix + 1]["id"]
            else:
                if section_ix < len(sections) - 1:
                    next_section_id = sections[section_ix + 1]["slug"]
                    next_question_id = None # intro
                else:
                    # Last question in last section — submit and go to confirmation
                    submission.submitted = True
                    submission.save()
                    del request.session["submission_id"]
                    request.session.pop("history", None)
                    return redirect(reverse("confirmation", kwargs={"lang": lang}))

        if next_question_id is None:
            next_url = reverse("section", kwargs={
                "lang": lang,
                "role": role,
                "section": next_section_id,
            })
        else:
            next_url = reverse("question", kwargs={
                "lang": lang,
                "role": role,
                "section": next_section_id,
                "question": next_question_id,
            })

        return redirect(next_url)
    
    prev_url = get_prev_url(request, lang, role, section_data["slug"], question_data["id"])

    # TODO: next prev (and how to measure progress across sections?)
    ctx = {
        "question": question_data,
        "field_value": getattr(submission, question_data["id"]) if submission else None,
        "prev_url": prev_url,
        "lang": lang,
        "role": role,
        "current_clinic_name_with_region": get_current_clinic_name_with_region(request, get_all_clinics()),
    }

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

@require_POST
def start_again(request):
    submission_id = request.session.get("submission_id")
    if submission_id:
        del request.session["submission_id"]

    return redirect(reverse("landing"))
