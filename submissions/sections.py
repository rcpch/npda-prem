from django.utils.translation import gettext as _

from .models import *


# Needs to be a function for translations to work properly
def build_sections():
    s1_demographics = {
        "slug": "demographics",
        "title": _("Demographics"),
        "introduction": _("demographics.introduction"),
        "roles": ["cyp", "parent"],
        "questions": [
            {
                "id": "q4_gender",
                "roles": ["cyp"],
                "title": {
                    "cyp": _("q4.child.title"),
                },
                "type": "radio",
                "options": GENDER_CHOICES,
            },
            {
                "id": "q5_relationship",
                "roles": ["parent"],
                "title": {
                    "parent": _("q5.parent.title"),
                },
                "type": "radio",
                "options": RELATIONSHIP_CHOICES,
            },
            {
                "id": "q6_diabetes_type",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q6.child.title"),
                    "parent": _("q6.parent.title"),
                },
                "type": "radio",
                "options": DIABETES_TYPE_CHOICES,
            },
            {
                "id": "q7_age_at_diagnosis",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q7.child.title"),
                    "parent": _("q7.parent.title"),
                },
                "type": "radio",
                "options": AGE_DIAGNOSIS_CHOICES,
            },
            {
                "id": "q8_ethnicity",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q8.child.title"),
                    "parent": _("q8.parent.title"),
                },
                "type": "radio",
                "options": ETHNICITY_CHOICES,
            },
            {
                "id": "q9_education_stage",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q9.child.title"),
                    "parent": _("q9.parent.title"),
                },
                "type": "radio",
                "options": EDUCATION_STAGE_CHOICES_WITH_HINTS,
                "next_question": {
                    "nursery": "q12_free_school_meals",
                    "_": "q10_school_type",
                }
            },
            {
                "id": "q10_school_type",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q10.child.title"),
                    "parent": _("q10.parent.title"),
                },
                "type": "radio",
                "options": SCHOOL_TYPE_CHOICES_WITH_HINTS,
                "next_question": {
                    "home": "q11_home_education_reason",
                    "_": "q12_free_school_meals",
                }
            },
            {
                "id": "q11_home_education_reason",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q11.child.title"),
                    "parent": _("q11.parent.title"),
                },
                "type": "radio",
                "options": HOME_ED_CHOICES,
            },
            {
                "id": "q12_free_school_meals",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q12.child.title"),
                    "parent": _("q12.parent.title"),
                },
                "type": "radio",
                "options": FREE_SCHOOL_MEALS_CHOICES,
            }
        ]
    }

    s2_healthcare_plans = {
        "slug": "healthcare_plans",
        "title": _("School Health Care Plans"),
        "introduction": _("healthcare_plans.introduction"),
        "roles": ["parent"],
        "questions": [
            {
                "id": "q13_healthcare_plan",
                "roles": ["parent"],
                "title": {
                    "parent": _("q13.parent.title"),
                },
                "hint": _("q13.hint"),
                "type": "radio",
                "options": YES_NO_DONTKNOW_CHOICES,
                "next_question": {
                    "yes": "q14_plan_coverage",
                    "_": "q15_school_contact",
                }
            },
            {
                "id": "q14_plan_coverage",
                "roles": ["parent"],
                "title": {
                    "parent": _("q14.parent.title"),
                },
                "type": "radio",
                "options": PLAN_COVERAGE_CHOICES,
            },
            {
                "id": "q15_school_contact",
                "roles": ["parent"],
                "title": {
                    "parent": _("q15.parent.title"),
                },
                "type": "radio",
                "options": YES_NO_DONTKNOW_CHOICES,
            },
        ]
    }

    s3_managing_diabetes = {
        "slug": "managing_diabetes",
        "title": _("Managing Diabetes"),
        "introduction": _("managing_diabetes.introduction"),
        "roles": ["cyp", "parent"],
        "questions": [
            {
                "id": "q16_insulin_or_monitor",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q16.child.title"),
                    "parent": _("q16.parent.title"),
                },
                "type": "radio",
                "options": YES_NO_CHOICES,
                "next_question": {
                    "yes": "q17_insulin_method",
                    "no": "q21_smartphone_use",
                }
            },
            {
                "id": "q17_insulin_method",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q17.child.title"),
                    "parent": _("q17.parent.title"),
                },
                "hint": _("q17.hint"),
                "type": "checkbox",
                "options": INSULIN_METHOD_OPTIONS,
            },
            {
                "id": "q18_glucose_monitoring",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q18.child.title"),
                    "parent": _("q18.parent.title"),
                },
                "hint": _("q18.hint"),
                "type": "checkbox",
                "options": GLUCOSE_MONITORING_OPTIONS,
            },
            {
                "id": "q19_remote_monitoring",
                "roles": ["parent"],
                "title": {
                    "parent": _("q19.parent.title"),
                },
                "type": "radio",
                "options": FREQUENCY_4_CHOICES,
            },
            {
                "id": "q20_contact_school",
                "roles": ["parent"],
                "title": {
                    "parent": _("q20.parent.title"),
                },
                "type": "radio",
                "options": FREQUENCY_5_CHOICES,
            },
            {
                "id": "q21_smartphone_use",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q21.child.title"),
                    "parent": _("q21.parent.title"),
                },
                "type": "radio",
                "options": FREQUENCY_4_NA_CHOICES,
            },
            {
                "id": "q22_private_room",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q22.child.title"),
                    "parent": _("q22.parent.title"),
                },
                "hint": _("q22.hint"),
                "type": "radio",
                "options": FREQUENCY_5_CHOICES,
            },
            {
                "id": "q23_classroom_management",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q23.child.title"),
                    "parent": _("q23.parent.title"),
                },
                "hint": _("q23.hint"),
                "type": "radio",
                "options": FREQUENCY_5_CHOICES,
            },
            {
                "id": "q24_trained_staff",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q24.child.title"),
                    "parent": _("q24.parent.title"),
                },
                "hint": _("q24.hint"),
                "type": "radio",
                "options": FREQUENCY_4_CHOICES,
            },
            {
                "id": "q25_carb_counting",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q25.child.title"),
                    "parent": _("q25.parent.title"),
                },
                "hint": _("q25.hint"),
                "type": "radio",
                "options": FREQUENCY_5_CHOICES,
            },
        ]
    }

    s4_education_impact = {
        "slug": "education_impact",
        "title": _("Impact on Education"),
        "introduction": _("education_impact.introduction"),
        "roles": ["cyp", "parent"],
        "questions": [
            {
                "id": "q26_missed_lessons",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q26.child.title"),
                    "parent": _("q26.parent.title"),
                },
                "hint": _("q26.hint"),
                "type": "number",
            },
            {
                "id": "q27_absences_authorised",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q27.child.title"),
                    "parent": _("q27.parent.title"),
                },
                "hint": _("q27.hint"),
                "type": "radio",
                "options": FREQUENCY_4_CHOICES,
            },
            {
                "id": "q28_attendance_impacted",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q28.child.title"),
                    "parent": _("q28.parent.title"),
                },
                "hint": _("q28.hint"),
                "type": "radio",
                "options": YES_NO_DONTKNOW_CHOICES,
            },
            {
                "id": "q29_days_off",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q29.child.title"),
                    "parent": _("q29.parent.title"),
                },
                "hint": _("q29.hint"),
                "type": "number",
            },
            {
                "id": "q30_moved_schools",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q30.child.title"),
                    "parent": _("q30.parent.title"),
                },
                "type": "radio",
                "options": YES_NO_CHOICES,
            },
            {
                "id": "q31_excluded_activities",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q31.child.title"),
                    "parent": _("q31.parent.title"),
                },
                "hint": _("q31.hint"),
                "type": "checkbox",
                "options": EXCLUDED_ACTIVITIES_OPTIONS,
            },
            {
                "id": "q32_performance_impact",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q32.child.title"),
                    "parent": _("q32.parent.title"),
                },
                "type": "radio",
                "options": FREQUENCY_6_CHOICES,
            },
            {
                "id": "q33_teacher_understanding",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q33.child.title"),
                    "parent": _("q33.parent.title"),
                },
                "hint": _("q33.hint"),
                "type": "radio",
                "options": FREQUENCY_5_CHOICES,
            },
            {
                "id": "q34_reasonable_adjustments",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q34.child.title"),
                    "parent": _("q34.parent.title"),
                },
                "hint": _("q34.hint"),
                "type": "radio",
                "options": YES_NO_NA_CHOICES,
            },
        ]
    }

    s5_wellbeing = {
        "slug": "wellbeing",
        "title": _("Social and Emotional Impact"),
        "introduction": _("wellbeing.introduction"),
        "roles": ["cyp", "parent"],
        "questions": [
            {
                "id": "q35_felt_left_out",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q35.child.title"),
                    "parent": _("q35.parent.title"),
                },
                "type": "radio",
                "options": FREQUENCY_6_CHOICES,
            },
            {
                "id": "q36_lost_income",
                "roles": ["parent"],
                "title": {
                    "parent": _("q36.parent.title"),
                },
                "hint": _("q36.hint"),
                "type": "radio",
                "options": YES_NO_NA_CHOICES,
            },
            {
                "id": "q37_anxiety_frequency",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q37.child.title"),
                    "parent": _("q37.parent.title"),
                },
                "type": "radio",
                "options": ANXIETY_CHOICES,
            },
            {
                "id": "q38_school_support",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q38.child.title"),
                    "parent": _("q38.parent.title"),
                },
                "type": "radio",
                "options": SUPPORT_CHOICES,
            },
            {
                "id": "q39_team_support",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q39.child.title"),
                    "parent": _("q39.parent.title"),
                },
                "type": "radio",
                "options": TEAM_SUPPORT_CHOICES,
            },
            {
                "id": "q40_worked_well",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q40.child.title"),
                    "parent": _("q40.parent.title"),
                },
                "hint": _("q40.hint"),
                "type": "textarea",
            },
            {
                "id": "q41_not_worked_well",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q41.child.title"),
                    "parent": _("q41.parent.title"),
                },
                "hint": _("q41.hint"),
                "type": "textarea",
            },
            {
                "id": "q42_improvements",
                "roles": ["cyp", "parent"],
                "title": {
                    "cyp": _("q42.child.title"),
                    "parent": _("q42.parent.title"),
                },
                "type": "textarea",
            },
        ]
    }

    sections = [
        s1_demographics,
        s2_healthcare_plans,
        s3_managing_diabetes,
        s4_education_impact,
        s5_wellbeing,
    ]

    return sections
