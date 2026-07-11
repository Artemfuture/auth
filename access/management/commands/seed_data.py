from django.core.management.base import BaseCommand

from access.models import (
    Role,
    Resource,
    Permission,
    RolePermission,
)


class Command(BaseCommand):
    help = "Заполняет БД начальными данными"

    def handle(self, *args, **kwargs):
        roles = [
            "Admin",
            "Manager",
            "User",
            "Guest",
        ]

        resources = [
            "Users",
            "Products",
            "Orders",
            "Stores",
            "AccessRules",
        ]

        permissions = [
            "READ",
            "CREATE",
            "UPDATE",
            "DELETE",
            "READ_ALL",
            "UPDATE_ALL",
            "DELETE_ALL",
        ]

        for role in roles:
            Role.objects.get_or_create(name=role)

        for resource in resources:
            Resource.objects.get_or_create(name=resource)

        for permission in permissions:
            Permission.objects.get_or_create(code=permission)

        self.stdout.write(self.style.SUCCESS("База успешно заполнена."))
        admin = Role.objects.get(name="Admin")
        manager = Role.objects.get(name="Manager")
        user = Role.objects.get(name="User")
        guest = Role.objects.get(name="Guest")
        for resource in Resource.objects.all():
            for permission in Permission.objects.all():
                RolePermission.objects.get_or_create(
                    role=admin,
                    resource=resource,
                    permission=permission,
                )
        orders = Resource.objects.get(name="Orders")

        for code in ["READ", "CREATE", "UPDATE"]:
            permission = Permission.objects.get(code=code)

            RolePermission.objects.get_or_create(
                role=user,
                resource=orders,
                permission=permission,
            )

        for resource_name in ["Orders", "Products"]:
            resource = Resource.objects.get(name=resource_name)

            for code in [
                "READ",
                "CREATE",
                "UPDATE",
                "READ_ALL",
                "UPDATE_ALL",
            ]:
                permission = Permission.objects.get(code=code)

                RolePermission.objects.get_or_create(
                    role=manager,
                    resource=resource,
                    permission=permission,
                )
        products = Resource.objects.get(name="Products")

        permission = Permission.objects.get(code="READ")

        RolePermission.objects.get_or_create(
            role=guest,
            resource=products,
            permission=permission,
        )
