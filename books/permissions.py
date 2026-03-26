from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        author_names = obj.authors.values_list('name', flat=True) #["ivan", "mitko", ...]
        return request.user and request.user.username in author_names