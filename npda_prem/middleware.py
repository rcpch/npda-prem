from django.conf import settings
from django.http import Http404
from django.utils import translation


class URLPathLanguageMiddleware:
    """Activate language from URL path prefix (e.g. /cy/form/parent/).

    Does NOT read cookies or Accept-Language headers.
    The landing page (/) defaults to English.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.valid_lang_codes = {code for code, _name in settings.LANGUAGES}

    def __call__(self, request):
        path_parts = request.path_info.strip("/").split("/")
        lang = path_parts[0] if path_parts[0] else None

        if lang and lang in self.valid_lang_codes:
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        elif lang and len(path_parts) > 1 and lang != "start-again":
            # Looks like a prefixed route but with an invalid language code
            raise Http404
        else:
            # Landing page, admin, or other unprefixed routes
            translation.activate("en")
            request.LANGUAGE_CODE = "en"

        response = self.get_response(request)
        return response
