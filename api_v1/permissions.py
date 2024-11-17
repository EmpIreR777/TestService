from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOfCart(BasePermission):
    """
    Разрешение, позволяющее доступ к корзине только
    её владельцу или сотрудникам.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
