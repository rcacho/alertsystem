from rest_framework import serializers
from alerts.models import User, GlucosePoint, Uploader


class GlucosePointSerializer(serializers.ModelSerializer):
    uploader = serializers.ReadOnlyField(source="uploader.id")

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
    uploader = UploaderSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'uploader']


