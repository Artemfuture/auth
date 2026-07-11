from access.models import (
    Permission,
    Resource,
    RolePermission,
    UserRole,
)


class PermissionService:
    @staticmethod
    def has_permission(user, resource_name, permission_code):
        if not user or not user.is_authenticated:
            return False

        try:
            resource = Resource.objects.get(name=resource_name)
            permission = Permission.objects.get(code=permission_code)
        except (Resource.DoesNotExist, Permission.DoesNotExist):
            return False

        roles = UserRole.objects.filter(user=user).values_list(
            "role_id",
            flat=True,
        )

        return RolePermission.objects.filter(
            role_id__in=roles,
            resource=resource,
            permission=permission,
        ).exists()

    @staticmethod
    def is_admin(user):
        if not user or not user.is_authenticated:
            return False

        return UserRole.objects.filter(
            user=user,
            role__name="Admin",
        ).exists()
