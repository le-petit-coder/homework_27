from rest_framework.permissions import BasePermission


class IsOwnerPermission(BasePermission):
    message = "You've got no permission to this selection"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False


class IsOwnerOrStuffPermission(BasePermission):
    message = "You've got no permission to this ad"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author or request.user.role in ["admin", "moderator"]:
            return True
        return False
