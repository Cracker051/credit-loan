from django.apps import AppConfig
from django.core.signals import setting_changed


class CreditConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend.credit"

    def ready(self):
        from backend.credit.signals import handle_request_status

        setting_changed.connect(handle_request_status)
