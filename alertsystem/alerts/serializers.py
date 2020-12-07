from rest_framework import serializers
from alerts.models import User, GlucosePoint, Uploader, \
    AlertSettings, FollowerInvitation


class FollowerInvitationReadSerializer(serializers.ModelSerializer):
    sent_by = serializers.ReadOnlyField(source="sent_by.email")
    sent_to = serializers.ReadOnlyField(source="sent_to.email")

    class Meta:
        model = FollowerInvitation
        fields = ['sent_by', 'sent_to', 'accepted', 'token']


class FollowerInvitationWriteSerializer(serializers.ModelSerializer):
    sent_to = serializers.EmailField()

    class Meta:
        model = FollowerInvitation
        fields = ['sent_by', 'sent_to']


class AlertSettingsReadSerializer(serializers.ModelSerializer):
    observer = serializers.ReadOnlyField(source="observer.owner.username")
    uploader = serializers.ReadOnlyField(source="observer.uploader.owner.username")

    class Meta:
        model = AlertSettings
        fields = ['observer', 'uploader', 'high_value', 'low_value']


class AlertSettingsWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AlertSettings
        fields = ['uploader_id', 'high_value', 'low_value']


class GlucosePointSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source="uploader.owner.username")

    class Meta:
        model = GlucosePoint
        fields = ['uploader', 'value', 'timestamp', 'created']


class UploaderSerializer(serializers.ModelSerializer):
    glucose_points = GlucosePointSerializer(many=True)
    diabetes_type = serializers.ChoiceField(Uploader.DiabetesType.choices)

    class Meta:
        model = Uploader
        fields = ['glucose_points', 'diabetes_type']


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(source="get_defining_role")

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


