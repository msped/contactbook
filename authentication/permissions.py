from rest_framework.permissions import BasePermission

class IsOwnerOfAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user
