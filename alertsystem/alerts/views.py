from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from alerts.serializers import UserSerializer, GlucosePointSerializer, \
    AlertSettingsReadSerializer, AlertSettingsWriteSerializer
from alerts.models import User, Uploader, GlucosePoint, AlertSettings
from alerts.permissions import IsUploaderOrFollower, IsUploader, IsObserver


class MultiSerializerViewMixin(object):
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except KeyError:
            return super(MultiSerializerViewMixin, self).get_serializer_class()


class FollowerInviteViewSet(viewsets.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsUploader]
        return [permissions for permissions in permission_classes]

    def list(self, request):
        if request.user.is_staff:
            return super().list(request)
        queryset = self.queryset.filter(uploader__owner__id=request.user.id)
        return Response(self.get_serializer(queryset).data)

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user.uploader)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request):
        if request.user.is_staff:
            return super().list(request)
        queryset = self.queryset.get(id=request.user.id)
        return Response(self.get_serializer(queryset).data)


class GlucosePointViewSet(viewsets.ModelViewSet):
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


class AlertSettingsViewSet(viewsets.ModelViewSet):
    queryset = AlertSettings.objects.all()
    serializer_class = AlertSettingsReadSerializer
    serializer_classes = {
        'list': AlertSettingsReadSerializer,
        'retrieve': AlertSettingsReadSerializer,
        'create': AlertSettingsWriteSerializer,
        'update': AlertSettingsWriteSerializer,
        'partial_update': AlertSettingsWriteSerializer,
        'destroy': AlertSettingsWriteSerializer,
    }
    permissions_classes = [IsObserver]

    def list(self, request):
        queryset = self.queryset.filter(observer__owner__id=self.request.user.id)
        return Response(self.get_serializer(queryset, many=True).data)

    def perform_create(self, serializer):
        serializer.save(observer=self.request.user.observing.get(
            uploader__owner__id=serializer.uploader_id),
            uploader=Uploader.objects.get(owner__id=serializer.uploader_id))
