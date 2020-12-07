from alerts.models import GlucosePoint, GlucoseAlert


def save_glucose_point(sender, instance, **kwargs):
    settings = instance.uploader.get_alert_settings()
    for setting in settings:
        alert = GlucoseAlert(observer=setting.observer,
                             glucose_point=instance)
        if instance.value > setting.high_value:
            alert.alert_type = GlucoseAlert.Type.High
            alert.save()
        if instance.value < setting.low_value:
            alert.alert_type = GlucoseAlert.Type.Low
            alert.save()


