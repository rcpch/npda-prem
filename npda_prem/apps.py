from django.contrib.admin.apps import AdminConfig


class CustomAdminConfig(AdminConfig):
    default_site = "npda_prem.admin_site.EntraAdminSite"
