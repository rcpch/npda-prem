from django.utils.translation import gettext as _

from .models import *

# Needs to be a function for translations to work properly
def build_sections():
    s1_demographics = {
        "slug": "demographics",
        "title": _("Demographics"),
        "template": "submissions/_child_demographics.html",
        "roles": ["cyp", "parent"],
        "questions": [
            {
                "id": "q4_gender",
                "roles": ["cyp"],
                "title": {
                    "cyp": _("q4.child.title"),
                    "parent": _("q4.parent.title"),
                },
                "type": "radio",
                "options": GENDER_CHOICES,
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
                "options": SCHOOL_TYPE_CHOICES,
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

    sections = [
        s1_demographics,
    ]

    return sections

    # return [
    #     {
    #         "slug": "healthcare-plans",
    #         "title": "School Health Care Plans",
    #         "template": "submissions/_parent_healthcare_plans.html",
    #         "roles": ["parent"],
    #     },
    #     {
    #         "slug": "managing-diabetes",
    #         "title": "Managing Diabetes",
    #         "template": "submissions/_child_managing_diabetes.html",
    #         "roles": ["cyp", "parent"],
    #     },
    #     {
    #         "slug": "education-impact",
    #         "title": "Impact on Education",
    #         "template": "submissions/_shared_education_impact.html",
    #         "roles": ["cyp", "parent"],
    #     },
    #     {
    #         "slug": "wellbeing",
    #         "title": "Social and Emotional Impact",
    #         "template": "submissions/_shared_wellbeing.html",
    #         "roles": ["cyp", "parent"],
    #     },
    # ]