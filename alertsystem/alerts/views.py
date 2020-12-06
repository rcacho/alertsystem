from rest_framework import viewsets, permissions, status
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
        return Response(self.get_serializer(queryset, many=True).data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user.uploader)