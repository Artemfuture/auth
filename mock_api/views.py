from rest_framework.response import Response
from rest_framework.views import APIView

from auth_system.permissions import permission_required


class OrdersView(APIView):
    @permission_required("Orders", "READ")
    def get(self, request):
        return Response(
            [
                {
                    "id": 1,
                    "title": "Order #1",
                    "owner": 1,
                },
                {
                    "id": 2,
                    "title": "Order #2",
                    "owner": 2,
                },
            ]
        )
