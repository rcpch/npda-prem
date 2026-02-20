from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()

def turnstile_form_embed():
    site_key = settings.TURNSTILE_SITE_KEY
    
    snippet = "<!-- Turnstile site key not configured -->"
    
    if site_key:
        snippet = f'<div class="cf-turnstile" data-sitekey="{site_key}" data-theme="light" data-appearance="interaction-only"></div>'

    return mark_safe(snippet)

register.simple_tag(turnstile_form_embed)