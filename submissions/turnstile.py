import logging
import requests

from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.conf import settings

logger = logging.getLogger(__name__)


def validate_turnstile(token, remoteip=None):
    if not settings.TURNSTILE_SECRET_KEY and token:
        logger.warning("Turnstile secret key not configured, but token provided")
        raise ImproperlyConfigured("Turnstile secret key not configured")
    
    if not settings.TURNSTILE_SECRET_KEY:
        logger.info("Turnstile secret key not configured, skipping validation")
        return True
    
    secret = settings.TURNSTILE_SECRET_KEY

    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'

    data = {
        'secret': secret,
        'response': token
    }

    if remoteip:
        data['remoteip'] = remoteip

    response = requests.post(url, data=data, timeout=10)
    response.raise_for_status()
    
    response_data = response.json()

    if not response_data.get("success", False):
        error_codes = response_data.get("error-codes", [])
        message = f"Unexpected Turnstile response: {error_codes}"

        logger.warning(message)
        raise SuspiciousOperation(message)
    
    return True