from django.db import models
from django.utils.translation import gettext_lazy as _


GENDER_CHOICES = [
    ("boy", _("q4.boy")),
    ("girl", _("q4.girl")),
    ("other", _("q4.other")),
    ("prefer-not-to-say", _("q4.prefer-not-to-say")),
]

DIABETES_TYPE_CHOICES = [
    ("type1", _("Type 1")),
    ("type2", _("Type 2")),
    ("other", _("Other")),
]

AGE_DIAGNOSIS_CHOICES = [
    ("0-3", _("3 years or younger")),
    ("4-7", _("4 – 7 years")),
    ("8-11", _("8 – 11 years")),
    ("12-16", _("12 – 16 years")),
    ("17-19", _("17 – 19 years")),
]

ETHNICITY_CHOICES = [
    ("white", _("White")),
    ("black", _("Black")),
    ("asian", _("Asian")),
    ("mixed", _("Mixed")),
    ("other", _("Other")),
    ("prefer-not-to-say", _("Prefer not to say")),
]

EDUCATION_STAGE_CHOICES_WITH_HINTS = [
    ("nursery", _("Nursery"), _("Ages < 4yrs")),
    ("reception", _("Reception"), _("Ages 4-5yrs")),
    ("ks1", _("Key stage 1 (Years 1 & 2)"), _("Ages 5-7yrs")),
    ("ks2", _("Key stage 2 (Years 3 to 6)"), _("Ages 7-11yrs")),
    ("ks3", _("Key stage 3 (Years 7 to 9)"), _("Ages 11-14yrs")),
    ("ks4", _("Key stage 4 (Years 10 & 11)"), _("Ages 14-16yrs")),
    ("ks5", _("Key stage 5 (Years 12 & 13)"), _("Ages 16-18yrs")),
    ("other", _("Other"), None),
]

EDUCATION_STAGE_CHOICES = [(value, label) for value, label, hint in EDUCATION_STAGE_CHOICES_WITH_HINTS]

SCHOOL_TYPE_CHOICES_WITH_HINTS = [
    ("state", _("State funded school"), _("q10.state.hint")),
    ("private", _("Private school"), _("q10.private.hint")),
    ("home", _("Home schooled/educated"), None),
]

SCHOOL_TYPE_CHOICES = [(value, label) for value, label, hint in SCHOOL_TYPE_CHOICES_WITH_HINTS]

HOME_ED_CHOICES = [
    ("no", _("No, it was for other reasons")),
    ("partly", _("Partly, the diabetes diagnosis influenced my decision")),
    ("yes", _("Yes, it was mainly because of the diabetes diagnosis")),
    ("prefer-not-to-say", _("Prefer not to say")),
]

FREE_SCHOOL_MEALS_CHOICES = [
    ("yes", _("Yes")),
    ("no", _("No")),
    ("dont-know", _("I don't know")),
    ("prefer-not-to-say", _("Prefer not to say")),
]

class Submission(models.Model):
    # -- Metadata ----------------------------------------------------------
    ROLE_CHOICES = [
        ("cyp", _("A child or young person with diabetes")),
        ("parent", _("The parent/carer of a child or young person with diabetes")),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    language = models.CharField(max_length=10, default="en")
    submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -- PZ code (canonical clinic identifier from selection flow) ----------
    pz_code = models.CharField(max_length=10, blank=True, default="")

    # -- Q3: Are you… (maps to role field above) ---------------------------

    # -- Q4: Gender (CYP only) --------------------------------------------
    q4_gender = models.CharField(
        max_length=20, choices=GENDER_CHOICES, blank=True, default="",
    )

    # -- Q5: Relationship to child (P/C only) -----------------------------
    RELATIONSHIP_CHOICES = [
        ("mother", _("Mother")),
        ("father", _("Father")),
        ("grandmother", _("Grandmother")),
        ("grandfather", _("Grandfather")),
        ("other", _("Other guardian or family member")),
    ]
    q5_relationship = models.CharField(
        max_length=20, choices=RELATIONSHIP_CHOICES, blank=True, default="",
    )

    # -- Q6: Diabetes type -------------------------------------------------
    q6_diabetes_type = models.CharField(
        max_length=10, choices=DIABETES_TYPE_CHOICES, blank=True, default="",
    )

    # -- Q7: Age at diagnosis ----------------------------------------------
    q7_age_at_diagnosis = models.CharField(
        max_length=10, choices=AGE_DIAGNOSIS_CHOICES, blank=True, default="",
    )

    # -- Q8: Ethnicity -----------------------------------------------------
    q8_ethnicity = models.CharField(
        max_length=20, choices=ETHNICITY_CHOICES, blank=True, default="",
    )

    # -- Q9: Education stage -----------------------------------------------
    q9_education_stage = models.CharField(
        max_length=20, choices=EDUCATION_STAGE_CHOICES, blank=True, default="",
    )
    q9_education_stage_other = models.CharField(
        max_length=200, blank=True, default="",
    )

    # -- Q10: School type --------------------------------------------------
    q10_school_type = models.CharField(
        max_length=10, choices=SCHOOL_TYPE_CHOICES, blank=True, default="",
    )

    # -- Q11: Home education related to diabetes (shown if Q10=home) -------
    q11_home_education_reason = models.CharField(
        max_length=20, choices=HOME_ED_CHOICES, blank=True, default="",
    )

    # -- Q12: Free school meals --------------------------------------------
    q12_free_school_meals = models.CharField(
        max_length=20, choices=FREE_SCHOOL_MEALS_CHOICES, blank=True, default="",
    )

    # -- Q13: School healthcare plan (P/C only) ----------------------------
    YES_NO_DONTKNOW_CHOICES = [
        ("yes", _("Yes")),
        ("no", _("No")),
        ("dont-know", _("I don't know")),
    ]
    q13_healthcare_plan = models.CharField(
        max_length=10, choices=YES_NO_DONTKNOW_CHOICES, blank=True, default="",
    )

    # -- Q14: Plan covers needs (P/C only, shown if Q13=yes) ---------------
    PLAN_COVERAGE_CHOICES = [
        ("yes", _("Yes")),
        ("partially", _("Partially covers diabetes needs at school")),
        ("no", _("No")),
        ("dont-know", _("I don't know")),
    ]
    q14_plan_coverage = models.CharField(
        max_length=12, choices=PLAN_COVERAGE_CHOICES, blank=True, default="",
    )

    # -- Q15: School has direct contact with diabetes team (P/C only) ------
    q15_school_contact = models.CharField(
        max_length=10, choices=YES_NO_DONTKNOW_CHOICES, blank=True, default="",
    )

    # -- Q16: Need to administer insulin / monitor in school ---------------
    YES_NO_CHOICES = [
        ("yes", _("Yes")),
        ("no", _("No")),
    ]
    q16_insulin_or_monitor = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, blank=True, default="",
    )

    # -- Q17: How administer insulin (multi-select, shown if Q16=yes) ------
    q17_insulin_method = models.JSONField(default=list, blank=True)

    # -- Q18: How monitor glucose (multi-select, shown if Q16=yes) ---------
    q18_glucose_monitoring = models.JSONField(default=list, blank=True)

    # -- Q19: Remote monitoring (P/C only) ---------------------------------
    FREQUENCY_4_CHOICES = [
        ("yes-always", _("Yes, always")),
        ("yes-sometimes", _("Yes, sometimes")),
        ("no-never", _("No, never")),
        ("dont-know", _("I don't know")),
    ]
    q19_remote_monitoring = models.CharField(
        max_length=15, choices=FREQUENCY_4_CHOICES, blank=True, default="",
    )

    # -- Q20: Contact school during day (P/C only) -------------------------
    FREQUENCY_5_CHOICES = [
        ("yes-always", _("Yes, always")),
        ("yes-sometimes", _("Yes, sometimes")),
        ("no-never", _("No, never")),
        ("dont-know", _("I don't know")),
        ("not-applicable", _("Not applicable")),
    ]
    q20_contact_school = models.CharField(
        max_length=15, choices=FREQUENCY_5_CHOICES, blank=True, default="",
    )

    # -- Q21: Smartphone/smartwatch use in school --------------------------
    FREQUENCY_4_NA_CHOICES = [
        ("yes-always", _("Yes, always")),
        ("yes-sometimes", _("Yes, sometimes")),
        ("no-never", _("No, never")),
        ("not-applicable", _("Not applicable")),
    ]
    q21_smartphone_use = models.CharField(
        max_length=15, choices=FREQUENCY_4_NA_CHOICES, blank=True, default="",
    )

    # -- Q22: Private room offered -----------------------------------------
    q22_private_room = models.CharField(
        max_length=15, choices=FREQUENCY_5_CHOICES, blank=True, default="",
    )

    # -- Q23: Manage diabetes in classroom ---------------------------------
    q23_classroom_management = models.CharField(
        max_length=15, choices=FREQUENCY_5_CHOICES, blank=True, default="",
    )

    # -- Q24: Trained staff ------------------------------------------------
    q24_trained_staff = models.CharField(
        max_length=15, choices=FREQUENCY_4_CHOICES, blank=True, default="",
    )

    # -- Q25: Carb-counting info -------------------------------------------
    q25_carb_counting = models.CharField(
        max_length=15, choices=FREQUENCY_5_CHOICES, blank=True, default="",
    )

    # -- Q26: Missed lessons (number) --------------------------------------
    q26_missed_lessons = models.CharField(max_length=10, blank=True, default="")

    # -- Q27: Absences authorised ------------------------------------------
    q27_absences_authorised = models.CharField(
        max_length=15, choices=FREQUENCY_4_CHOICES, blank=True, default="",
    )

    # -- Q28: Attendance records impacted ----------------------------------
    q28_attendance_impacted = models.CharField(
        max_length=10, choices=YES_NO_DONTKNOW_CHOICES, blank=True, default="",
    )

    # -- Q29: Days off school (number) -------------------------------------
    q29_days_off = models.CharField(max_length=10, blank=True, default="")

    # -- Q30: Had to move schools ------------------------------------------
    q30_moved_schools = models.CharField(
        max_length=5, choices=YES_NO_CHOICES, blank=True, default="",
    )

    # -- Q31: Excluded from activities (multi-select) ----------------------
    q31_excluded_activities = models.JSONField(default=list, blank=True)
    q31_excluded_activities_other = models.CharField(
        max_length=200, blank=True, default="",
    )

    # -- Q32: Performance impact -------------------------------------------
    FREQUENCY_6_CHOICES = [
        ("never", _("Never")),
        ("rarely", _("Rarely")),
        ("sometimes", _("Sometimes")),
        ("often", _("Often")),
        ("always", _("Always")),
        ("dont-know", _("I don't know")),
    ]
    q32_performance_impact = models.CharField(
        max_length=15, choices=FREQUENCY_6_CHOICES, blank=True, default="",
    )

    # -- Q33: Teacher understanding ----------------------------------------
    q33_teacher_understanding = models.CharField(
        max_length=15, choices=FREQUENCY_5_CHOICES, blank=True, default="",
    )

    # -- Q34: Reasonable adjustments offered -------------------------------
    YES_NO_NA_CHOICES = [
        ("yes", _("Yes")),
        ("no", _("No")),
        ("not-applicable", _("Not applicable")),
    ]
    q34_reasonable_adjustments = models.CharField(
        max_length=15, choices=YES_NO_NA_CHOICES, blank=True, default="",
    )

    # -- Q35: Felt left out ------------------------------------------------
    q35_felt_left_out = models.CharField(
        max_length=15, choices=FREQUENCY_6_CHOICES, blank=True, default="",
    )

    # -- Q36: Lost income (P/C only) ---------------------------------------
    q36_lost_income = models.CharField(
        max_length=15, choices=YES_NO_NA_CHOICES, blank=True, default="",
    )

    # -- Q37: Anxiety/stress frequency -------------------------------------
    ANXIETY_CHOICES = [
        ("never", _("Never")),
        ("less-than-weekly", _("Less than once a week")),
        ("once-or-twice", _("Once or twice a week")),
        ("three-or-four", _("Three or four times a week")),
        ("every-day", _("Every day of the week")),
    ]
    q37_anxiety_frequency = models.CharField(
        max_length=20, choices=ANXIETY_CHOICES, blank=True, default="",
    )

    # -- Q38: School support rating ----------------------------------------
    SUPPORT_CHOICES = [
        ("very-well", _("Very well supported")),
        ("well", _("Well supported")),
        ("neutral", _("Neutral")),
        ("poorly", _("Poorly supported")),
        ("very-poorly", _("Very poorly supported")),
        ("not-applicable", _("Not applicable")),
    ]
    q38_school_support = models.CharField(
        max_length=15, choices=SUPPORT_CHOICES, blank=True, default="",
    )

    # -- Q39: Diabetes team support rating ---------------------------------
    TEAM_SUPPORT_CHOICES = [
        ("very-well", _("Very well supported")),
        ("well", _("Well supported")),
        ("neutral", _("Neutral")),
        ("poorly", _("Poorly supported")),
        ("very-poorly", _("Very poorly supported")),
    ]
    q39_team_support = models.CharField(
        max_length=15, choices=TEAM_SUPPORT_CHOICES, blank=True, default="",
    )

    # -- Q40–42: Free text -------------------------------------------------
    q40_worked_well = models.TextField(blank=True, default="")
    q41_not_worked_well = models.TextField(blank=True, default="")
    q42_improvements = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Submission {self.pk} ({self.get_role_display()}, submitted={self.submitted})"
