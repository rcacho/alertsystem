from rest_framework import viewsets, permissions
from rest_framework.response import Response
from alerts.serializers import UserSerializer, GlucosePointSerializer
from alerts.models import User, GlucosePoint
from alerts.permissions import IsUploaderOrFollower


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class GlucosePointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlucosePoint.objects.all()
    serializer_class = GlucosePointSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsUploaderOrFollower]

    def list(self, request):
        queryset = self.queryset.filter(uploader__id=request.user.uploader.id)
        return Response(self.serializer_class(queryset, many=True).data)
