from django.apps import AppConfig


class SiteSettingsConfig(AppConfig):
    name = "site_settings"
    
    def ready(self):
        from . import signals
