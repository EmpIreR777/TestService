from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsStaffOrAuthenticatedUserOrReadOnly(BasePermission):
    """
    Разрешение, позволяющее доступ к объекту
    только авторизованным пользователям или сотрудникам.
    Чтение доступно всем (методы SAFE_METHODS).
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or request.user.is_authenticated and request.user.is_staff)


class IsOwnerOfCart(BasePermission):
    """
    Разрешение, позволяющее доступ к корзине только
    её владельцу или сотрудникам.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff
