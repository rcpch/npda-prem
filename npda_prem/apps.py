from django.contrib.admin import AdminConfig


class CustomAdminConfig(AdminConfig):
    default_site = "npda_prem.admin_site.EntraAdminSite"
