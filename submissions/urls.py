from django.urls import path

from . import views

urlpatterns = [
    # Landing page -- no language prefix, always English
    path("", views.landing, name="landing"),
    # All other pages under /<lang>/...
    path("<str:lang>/clinic-or-region", views.clinic_or_region, name="clinic_or_region"),
    path("<str:lang>/clinic-in-region/<slug:region>/", views.clinic_in_region, name="clinic_in_region"),
    path("<str:lang>/role/", views.role_form, name="role_form"),
    # Parent form
    path("<str:lang>/parent/", views.parent_form, name="parent_form"),
    path("<str:lang>/parent/<slug:section>/", views.parent_form, name="parent_form_section"),
    # Child form
    path("<str:lang>/child/", views.child_form, name="child_form"),
    path("<str:lang>/child/<slug:section>/", views.child_form, name="child_form_section"),
    path("<str:lang>/autosave/<slug:role>", views.autosave, name="autosave"),
    path("<str:lang>/submit/<slug:role>", views.submit, name="submit"),
    # Done!
    path("<str:lang>/confirmation/", views.confirmation, name="confirmation"),
    # Other
    path("/start-again/", views.start_again, name="start_again"),
]
