from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("form/", views.submission_form, name="submission_form"),
    # Parent form
    path("form/parent/", views.parent_form, name="parent_form"),
    path("form/parent/autosave/", views.parent_autosave, name="parent_autosave"),
    path("form/parent/submit/", views.parent_submit, name="parent_submit"),
    path("form/parent/<slug:section>/", views.parent_form, name="parent_form_section"),
    # Child form
    path("form/child/", views.child_form, name="child_form"),
    path("form/child/autosave/", views.child_autosave, name="child_autosave"),
    path("form/child/submit/", views.child_submit, name="child_submit"),
    path("form/child/<slug:section>/", views.child_form, name="child_form_section"),
    # Other
    path("form/start-again/", views.start_again, name="start_again"),
    path("form/confirmation/", views.confirmation, name="confirmation"),
]
