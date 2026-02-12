from django.urls import path

from . import views

urlpatterns = [
    # Landing page -- no language prefix, always English
    path("", views.landing, name="landing"),
    # All other pages under /<lang>/...
    path("<str:lang>/form/", views.region_form, name="submission_form"),
    path("<str:lang>/form/clinic/", views.clinic_form, name="clinic_form"),
    path("<str:lang>/form/role/", views.role_form, name="role_form"),
    # Parent form
    path("<str:lang>/form/parent/", views.parent_form, name="parent_form"),
    path("<str:lang>/form/parent/autosave/", views.parent_autosave, name="parent_autosave"),
    path("<str:lang>/form/parent/submit/", views.parent_submit, name="parent_submit"),
    path("<str:lang>/form/parent/<slug:section>/", views.parent_form, name="parent_form_section"),
    # Child form
    path("<str:lang>/form/child/", views.child_form, name="child_form"),
    path("<str:lang>/form/child/autosave/", views.child_autosave, name="child_autosave"),
    path("<str:lang>/form/child/submit/", views.child_submit, name="child_submit"),
    path("<str:lang>/form/child/<slug:section>/", views.child_form, name="child_form_section"),
    # Other
    path("<str:lang>/form/start-again/", views.start_again, name="start_again"),
    path("<str:lang>/form/confirmation/", views.confirmation, name="confirmation"),
]
