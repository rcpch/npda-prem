from django.urls import path

from . import views

urlpatterns = [
    # Landing page -- no language prefix, always English
    path("", views.landing, name="landing"),
    # All other pages under /<lang>/...
    path("<str:lang>/clinic-or-region", views.clinic_or_region, name="clinic_or_region"),
    path("<str:lang>/clinic-in-region/<slug:region>/", views.clinic_in_region, name="clinic_in_region"),
    path("<str:lang>/role/", views.role_form, name="role_form"),
    path("<str:lang>/confirmation/", views.confirmation, name="confirmation"),
    path("<str:lang>/<slug:role>/", views.form, name="form"),
    path("<str:lang>/<slug:role>/autosave/", views.autosave, name="autosave"),
    path("<str:lang>/<slug:role>/submit/", views.submit, name="submit"),
    path("<str:lang>/<slug:role>/<slug:section>/", views.section, name="section"),
    path("<str:lang>/<slug:role>/<slug:section>/<slug:question>/", views.question, name="question"),
    # Done!
    # Other
    path("start-again/", views.start_again, name="start_again"),
]
