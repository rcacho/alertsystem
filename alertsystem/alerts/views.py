from rest_framework import viewsets, permissions
from alerts.serializers import UserSerializer, GlucosePointSerializer
from alerts.models import User, GlucosePoint
from alerts.permissions import IsUploaderOrFollower


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GlucosePointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlucosePoint.objects.all()
    serializer_class = GlucosePointSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsUploaderOrFollower]
