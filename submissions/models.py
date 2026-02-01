from django.db import models


class Submission(models.Model):
    ROLE_CHOICES = [
        ("parent", "Parent"),
        ("child", "Child"),
    ]

    RATING_CHOICES = [
        ("very-good", "Very good"),
        ("good", "Good"),
        ("neither", "Neither good nor poor"),
        ("poor", "Poor"),
        ("very-poor", "Very poor"),
    ]

    HOSPITAL_CHOICES = [
        ("hospital-1", "Hospital 1"),
        ("hospital-2", "Hospital 2"),
        ("hospital-3", "Hospital 3"),
    ]

    # Metadata
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    language = models.CharField(max_length=10, default="en")
    submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Survey fields
    contact = models.JSONField(default=list, blank=True)
    rating = models.CharField(max_length=20, choices=RATING_CHOICES, blank=True, default="")
    hospital = models.CharField(max_length=20, choices=HOSPITAL_CHOICES, blank=True, default="")
    child_age = models.CharField(max_length=10, blank=True, default="")
    comments = models.TextField(blank=True, default="")

    def __str__(self):
        return f"Submission {self.pk} ({self.role}, submitted={self.submitted})"
