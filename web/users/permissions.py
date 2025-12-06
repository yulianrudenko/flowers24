from rest_framework.permissions import IsAuthenticated


class IsSelfOrAdmin(IsAuthenticated):
    def has_object_permission(self, request, view, obj) -> bool:  # type: ignore
        if not super().has_permission(request, view):
            return False

        if request.user.is_staff:
            return True

        return obj.id == request.user.id
