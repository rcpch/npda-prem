# local storage for current user - will not work in async contexts
# This is used to track the user making changes in the admin interface as well as in the view by storing 
# the user in thread-local storage. 

import logging
from datetime import datetime
from threading import local
from timeit import default_timer as timer
from django.conf import settings

request_logger = logging.getLogger("npda_request_log")

class NPDARequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = timer()

        response = self.get_response(request)

        end = timer()

        duration = end - start
        duration_ms = round(duration * 1000)

        # The dev server already does request logging
        if settings.ENABLE_REQUEST_LOGGING:
            # This replaces the old gunicorn request logging which used this date format string
            gunicorn_formatted_datetime = datetime.now().astimezone().strftime("%d/%m/%y:%H:%M:%S %z")

            request_logger.info(f"{request.META.get('HTTP_X_FORWARDED_FOR', '')} - [{gunicorn_formatted_datetime}] \"{request.method} {request.get_full_path()}\" {response.status_code} {response.get('Content-Length', "-")} \"{request.META.get('HTTP_REFERER', '-')}\" \"{request.META.get('HTTP_USER_AGENT', '-')}\" {duration_ms}")

        return response
