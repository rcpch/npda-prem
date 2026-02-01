from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .models import Submission


def _get_lang(request):
    return request.GET.get("lang", "en")


def _lang_qs(request):
    return f"?lang={_get_lang(request)}"


def landing(request):
    return render(request, "submissions/landing.html")


def submission_form(request):
    return render(request, "submissions/form.html")


def parent_form(request):
    submission = None
    submission_id = request.session.get("submission_id")

    if submission_id:
        try:
            submission = Submission.objects.get(
                pk=submission_id, role="parent", submitted=False
            )
        except Submission.DoesNotExist:
            del request.session["submission_id"]

    return render(request, "submissions/parent_form.html", {"submission": submission})


@require_POST
def parent_autosave(request):
    submission_id = request.session.get("submission_id")
    submission = None

    if submission_id:
        try:
            submission = Submission.objects.get(pk=submission_id, submitted=False)
        except Submission.DoesNotExist:
            pass

    if submission is None:
        submission = Submission.objects.create(
            role="parent",
            language=_get_lang(request),
        )
        request.session["submission_id"] = submission.pk

    field_map = {
        "rating": "rating",
        "hospital": "hospital",
        "child_age": "child_age",
        "comments": "comments",
    }

    for post_key, model_field in field_map.items():
        if post_key in request.POST:
            setattr(submission, model_field, request.POST[post_key])

    if "contact" in request.POST:
        submission.contact = [v for v in request.POST.getlist("contact") if v]

    submission.save()

    return HttpResponse(status=204)


@require_POST
def parent_submit(request):
    submission_id = request.session.get("submission_id")

    if not submission_id:
        return redirect(reverse("parent_form") + _lang_qs(request))

    submission = get_object_or_404(Submission, pk=submission_id, submitted=False)
    submission.submitted = True
    submission.save()

    del request.session["submission_id"]

    return redirect(reverse("confirmation") + _lang_qs(request))


def start_again(request):
    submission_id = request.session.get("submission_id")
    if submission_id:
        Submission.objects.filter(pk=submission_id, submitted=False).delete()
        del request.session["submission_id"]

    return redirect(reverse("landing"))


def confirmation(request):
    return render(request, "submissions/confirmation.html")


def child_form(request):
    return render(request, "submissions/child_form.html")
