from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel


class User(AbstractUser):
    class Role(models.TextChoices):
        Admin = 0
        Basic = 1

    role = models.IntegerField(choices=Role.choices, default=Role.Basic)

    def has_data_access(self, user_id):
        if self.uploader is not None and self.id == user_id:
            return True
        if len(self.observing.filter(uploader__owner__id=user_id)):
            return True
        return False


class Uploader(models.Model):
    class DiabetesType(models.IntegerChoices):
        none = 0
        type1 = 1
        type2 = 2
        pre = 3

    owner = models.OneToOneField(User, related_name="uploader", on_delete=models.CASCADE)
    diabetes_type = models.IntegerField(choices=DiabetesType.choices,
                                        default=DiabetesType.none)


class Observer(models.Model):
    class Status(models.IntegerChoices):
        Following = 1
        Blocked = 2

    owner = models.ForeignKey(User, related_name="observing",
                              on_delete=models.CASCADE)
    uploader = models.ForeignKey(Uploader, related_name="follower",
                                 on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices, default=Status.Following)
    accepted = models.BooleanField(default=False)


class GlucosePoint(TimeStampedModel):
    value = models.IntegerField()
    timestamp = models.DateTimeField()
    device_data = models.JSONField()
    uploader = models.ForeignKey('alerts.Uploader', related_name='glucose_points', on_delete=models.CASCADE)

    class Meta:
        ordering = ['timestamp']
