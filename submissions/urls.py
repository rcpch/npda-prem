from django.urls import path

from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("form/", views.submission_form, name="submission_form"),
]
