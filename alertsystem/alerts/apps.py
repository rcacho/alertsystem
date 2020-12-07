from django.apps import AppConfig
from django.db.models.signals import post_save


class AlertsConfig(AppConfig):
    name = 'alerts'

    def ready(self):
        from alerts.models import GlucosePoint
        from alerts.signals import save_glucose_point
        post_save.connect(save_glucose_point, sender=GlucosePoint)
