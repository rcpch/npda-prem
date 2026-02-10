from django.conf import settings
from django.utils import translation


class QueryStringLanguageMiddleware:
    """Activate language from ?lang= query parameter and persist via cookie."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.GET.get("lang")
        valid_codes = [code for code, name in settings.LANGUAGES]
        if lang and lang in valid_codes:
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        if lang and lang in valid_codes:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        return response
