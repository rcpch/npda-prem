from django.utils.translation import gettext as _

from .models import *

# Needs to be a function for translations to work properly
def build_sections():
    return [
        {
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
                    "next_question": "q6_diabetes_type",
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
                    "next_question": "q7_age_at_diagnosis",
                }
            ]
        },
        {
            "slug": "healthcare-plans",
            "title": "School Health Care Plans",
            "template": "submissions/_parent_healthcare_plans.html",
            "roles": ["parent"],
        },
        {
            "slug": "managing-diabetes",
            "title": "Managing Diabetes",
            "template": "submissions/_child_managing_diabetes.html",
            "roles": ["cyp", "parent"],
        },
        {
            "slug": "education-impact",
            "title": "Impact on Education",
            "template": "submissions/_shared_education_impact.html",
            "roles": ["cyp", "parent"],
        },
        {
            "slug": "wellbeing",
            "title": "Social and Emotional Impact",
            "template": "submissions/_shared_wellbeing.html",
            "roles": ["cyp", "parent"],
        },
    ]