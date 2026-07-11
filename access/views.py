from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RolePermission
from .serializers import RolePermissionSerializer
from .services import PermissionService


class RolePermissionListView(APIView):
    def get(self, request):
        if request.user is None:
            return Response(status=401)

        if not PermissionService.is_admin(request.user):
            return Response(status=403)

        serializer = RolePermissionSerializer(
            RolePermission.objects.all(),
            many=True,
        )

        return Response(serializer.data)


class RolePermissionCreateView(APIView):
    def post(self, request):
        if request.user is None:
            return Response(status=401)

        if not PermissionService.is_admin(request.user):
            return Response(status=403)

        serializer = RolePermissionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            serializer.data,
            status=201,
        )


class RolePermissionUpdateView(APIView):
    def put(self, request, pk):
        if request.user is None:
            return Response(status=401)

        if not PermissionService.is_admin(request.user):
            return Response(status=403)

        rule = RolePermission.objects.get(pk=pk)

        serializer = RolePermissionSerializer(
            rule,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class RolePermissionDeleteView(APIView):
    def delete(self, request, pk):
        if request.user is None:
            return Response(status=401)

        if not PermissionService.is_admin(request.user):
            return Response(status=403)

        RolePermission.objects.get(pk=pk).delete()

        return Response(status=204)
