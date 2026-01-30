from django.shortcuts import render


def landing(request):
    return render(request, "submissions/landing.html")


def submission_form(request):
    return render(request, "submissions/form.html")
