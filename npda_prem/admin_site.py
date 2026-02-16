import logging

import msal
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_not_required
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

logger = logging.getLogger(__name__)
User = get_user_model()


def _get_msal_app():
    authority = f"https://login.microsoftonline.com/{settings.ADMIN_LOGIN_AZURE_TENANT_ID}"
    return msal.ConfidentialClientApplication(
        client_id=settings.ADMIN_LOGIN_AZURE_CLIENT_ID,
        client_credential=settings.ADMIN_LOGIN_AZURE_CLIENT_SECRET or None,
        authority=authority,
    )


class EntraAdminSite(admin.AdminSite):
    """AdminSite that authenticates via Microsoft Entra ID OAuth 2 with PKCE."""

    def get_urls(self):
        custom_urls = [
            path(
                "oauth/callback/",
                self.admin_site_oauth_callback,
                name="oauth_callback",
            ),
        ]
        return custom_urls + super().get_urls()

    @method_decorator(never_cache)
    @method_decorator(login_not_required)
    def login(self, request, extra_context=None):
        if request.method == "GET" and self.has_permission(request):
            return HttpResponseRedirect(reverse("admin:index", current_app=self.name))

        msal_app = _get_msal_app()
        redirect_uri = request.build_absolute_uri(
            reverse("admin:oauth_callback", current_app=self.name)
        )
        flow = msal_app.initiate_auth_code_flow(
            scopes=["User.Read"],
            redirect_uri=redirect_uri,
        )
        request.session["oauth_flow"] = flow
        return HttpResponseRedirect(flow["auth_uri"])

    @method_decorator(never_cache)
    @method_decorator(login_not_required)
    def admin_site_oauth_callback(self, request):
        flow = request.session.pop("oauth_flow", None)
        if not flow:
            logger.warning("OAuth callback with no flow in session")
            return HttpResponseRedirect(reverse("admin:login"))

        msal_app = _get_msal_app()
        try:
            result = msal_app.acquire_token_by_auth_code_flow(flow, request.GET)
        except ValueError:
            logger.warning("OAuth state validation failed")
            return HttpResponseRedirect(reverse("admin:login"))

        if "error" in result:
            logger.error(
                "OAuth error: %s - %s",
                result.get("error"),
                result.get("error_description"),
            )
            return HttpResponseRedirect(reverse("admin:login"))

        id_claims = result.get("id_token_claims", {})
        email = (
            id_claims.get("preferred_username")
            or id_claims.get("email")
            or ""
        ).lower().strip()

        if not email or email not in settings.ADMIN_ALLOWED_EMAILS:
            logger.warning("Access denied for email: %s", email)
            context = {
                **self.each_context(request),
                "title": "Access denied",
                "email": email,
            }
            return TemplateResponse(
                request, "admin/oauth_denied.html", context, status=403
            )

        user, created = User.objects.get_or_create(
            username=email,
            defaults={
                "email": email,
                "is_staff": True,
                "is_superuser": True,
                "first_name": id_claims.get("given_name", ""),
                "last_name": id_claims.get("family_name", ""),
            },
        )
        if not created:
            changed = False
            if not user.is_staff:
                user.is_staff = True
                changed = True
            if not user.is_superuser:
                user.is_superuser = True
                changed = True
            if changed:
                user.save(update_fields=["is_staff", "is_superuser"])

        if not user.has_usable_password():
            user.set_unusable_password()
            user.save(update_fields=["password"])

        login(request, user)
        return HttpResponseRedirect(reverse("admin:index"))


entra_admin_site = EntraAdminSite(name="admin")
