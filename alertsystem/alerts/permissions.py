from rest_framework import permissions


class IsUploaderOrFollower(permissions.BasePermission):
    def has_object_permissions(self, request, view, obj):
        if request.user.Role == 0:
            return True
        if request.user.has_data_access(obj.uploader.owner.id):
            return True

