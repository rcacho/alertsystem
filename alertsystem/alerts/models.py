import random, string
from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel


class User(AbstractUser):
    class Role(models.TextChoices):
        Admin = 0
        Basic = 1

    email = models.EmailField(max_length=50, unique=True)
    role = models.IntegerField(choices=Role.choices, default=Role.Basic)

    def is_uploader(self, user_id):
        return hasattr(self, 'uploader') and self.id == user_id

    def is_observer(self, user_id):
        return len(self.observing.filter(uploader__owner__id=user_id)) > 0

    def get_defining_role(self):
        if self.role == User.Role.Admin:
            return 'admin'
        if hasattr(self, 'uploader'):
            return 'uploader'
        if any([_ for _ in self.observing.all() if id != self.id]):
            return 'follower'
        return 'basic'


class Uploader(models.Model):
    class DiabetesType(models.IntegerChoices):
        none = 0
        type1 = 1
        type2 = 2
        pre = 3

    owner = models.OneToOneField(User, related_name="uploader", on_delete=models.CASCADE)
    diabetes_type = models.IntegerField(choices=DiabetesType.choices,
                                        default=DiabetesType.none)

    def get_alert_settings(self):
        return [follower.alert_settings for follower in self.followers.all()]


class Observer(models.Model):
    class Status(models.IntegerChoices):
        Following = 1
        Blocked = 2

    owner = models.ForeignKey(User, related_name="observing",
                              on_delete=models.CASCADE)
    uploader = models.ForeignKey(Uploader, related_name="followers",
                                 on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices, default=Status.Following)
    accepted = models.BooleanField(default=False)


def generate_follower_token():
    return ''.join(random.choice(string.ascii_uppercase + string.digits, k=12))


class FollowerInvitation(models.Model):
    sent_by = models.ForeignKey(Uploader, related_name="follower_invitations_sent",
                                on_delete=models.CASCADE)
    sent_to = models.ForeignKey(User, related_name="follow_invitations_received",
                                on_delete=models.CASCADE)
    token = models.CharField(max_length=35,
                             default=generate_follower_token())
    accepted = models.BooleanField(default=False)


class GlucosePoint(TimeStampedModel):
    value = models.IntegerField()
    timestamp = models.DateTimeField()
    device_data = models.JSONField(null=True)
    uploader = models.ForeignKey('alerts.Uploader',
                                 related_name='glucose_points', on_delete=models.CASCADE)

    class Meta:
        ordering = ['timestamp']


class AlertSettings(TimeStampedModel):
    observer = models.OneToOneField('alerts.Observer',
                                    related_name='alert_settings', on_delete=models.CASCADE)
    high_value = models.IntegerField(default=180)
    low_value = models.IntegerField(default=70)


class GlucoseAlert(TimeStampedModel):
    class Type(models.IntegerChoices):
        Low = 1
        High = 2

    observer = models.ForeignKey('alerts.Observer',
                                 related_name='high_alerts', on_delete=models.CASCADE)
    glucose_point = models.ForeignKey('alerts.GlucosePoint', on_delete=models.CASCADE)
    alert_type = models.IntegerField(choices=Type.choices)
