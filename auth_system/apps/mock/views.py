from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.access.permissions import HasPermissionCode

class OrdersView(APIView):
    permission_classes = [IsAuthenticated, HasPermissionCode("orders.read")]

    def get(self, request):
        return Response([
            {"id": 1, "title": "Заказ #1"},
            {"id": 2, "title": "Заказ #2"},
        ])

class ReportsView(APIView):
    permission_classes = [IsAuthenticated, HasPermissionCode("reports.view")]

    def get(self, request):
        return Response([
            {"id": 10, "name": "Отчет по продажам"},
        ])