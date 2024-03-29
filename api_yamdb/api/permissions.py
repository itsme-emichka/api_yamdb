from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from django.http import HttpRequest
from django.db.models import Model


class IsAuthAdmin(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: ModelViewSet) -> bool:
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsAuthAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: ModelViewSet) -> bool:
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_admin
        )


class AuthAuthorAdminModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: ModelViewSet) -> bool:
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
        )

    def has_object_permission(
        self, request: HttpRequest, view: ModelViewSet, obj: Model
    ) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or (
            request.user.is_moderator or request.user.is_admin)
