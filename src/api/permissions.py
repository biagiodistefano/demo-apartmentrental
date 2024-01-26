from ninja_extra import permissions
from django.http.request import HttpRequest


class IsRealtor(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, **kwargs) -> bool:  # type: ignore
        if request.user.is_anonymous:  # pragma: no cover
            return False  # note: it's just for completeness, it's not possible to reach this code
        return request.user.groups.filter(name="realtor").exists()
