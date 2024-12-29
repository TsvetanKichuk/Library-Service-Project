from rest_framework.permissions import BasePermission, IsAuthenticated


class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.borrowing_id.user_id == request.user


class IsAdminUserOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return request.user.is_staff
