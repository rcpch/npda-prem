from django.urls import path

from . import views

urlpatterns = [
    # Landing page -- no language prefix, always English
    path("", views.landing, name="landing"),
    path("tablet-mode/", views.tablet_mode, name="tablet_mode"),
    # All other pages under /<lang>/...
    path("<str:lang>/introduction/", views.front_matter, name="front_matter"),
    path("<str:lang>/clinic-or-region", views.clinic_or_region, name="clinic_or_region"),
    path("<str:lang>/clinic-in-region/<slug:region>/", views.clinic_in_region, name="clinic_in_region"),
    path("<str:lang>/role/", views.role_form, name="role_form"),
    path("<str:lang>/confirmation/", views.confirmation, name="confirmation"),
    path("<str:lang>/<slug:role>/submit/", views.submit, name="submit"),
    path("<str:lang>/<slug:role>/<slug:section>/<slug:question>/", views.question, name="question"),
    # Done!
    # Other
    path("resume/", views.resume_or_new, name="resume_or_new"),
    path("start-again/", views.start_again, name="start_again"),
]
