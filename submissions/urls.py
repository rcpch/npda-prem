from django.urls import path

from . import views

urlpatterns = [
    # Landing page -- no language prefix, always English
    path("", views.landing, name="landing"),
    # All other pages under /<lang>/...
    path("<str:lang>/form/clinic-or-region", views.clinic_or_region, name="clinic_or_region"),
    path("<str:lang>/form/clinic-in-region/", views.clinic_in_region, name="clinic_in_region"),
    path("<str:lang>/form/role/", views.role_form, name="role_form"),
    # Parent form
    path("<str:lang>/form/parent/", views.parent_form, name="parent_form"),
    path("<str:lang>/form/parent/submit/", views.parent_submit, name="parent_submit"),
    path("<str:lang>/form/parent/<slug:section>/", views.parent_form, name="parent_form_section"),
    # Child form
    path("<str:lang>/form/child/", views.child_form, name="child_form"),
    path("<str:lang>/form/child/submit/", views.child_submit, name="child_submit"),
    path("<str:lang>/form/child/<slug:section>/", views.child_form, name="child_form_section"),
    path("<str:lang>/autosave/<slug:role>", views.autosave, name="autosave"),
    # Other
    path("/start-again/", views.start_again, name="start_again"),
    path("<str:lang>/form/confirmation/", views.confirmation, name="confirmation"),
]
