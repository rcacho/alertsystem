from rest_framework import permissions
from alerts.models import User


class IsUploaderOrFollower(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        if request.user.Role == User.Role.Admin or request.user.is_uploader(obj.uploader.owner.id):
            return True
        if request.user.is_observer(obj.uploader.owner.id) and request.method in permissions.SAFE_METHODS:
            return True
        return False


class IsObserver(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        if request.user.Role == User.Role.Admin or request.user.id == obj.observer.owner.id:
            return True
        return False
