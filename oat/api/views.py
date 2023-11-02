from rest_framework import viewsets

from orders.models import Order
from .serializers import OrderCreateSerializer, OrderCloseSerializer


class OrderCreateViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return OrderCloseSerializer
        return OrderCreateSerializer

    # Делал для корректного вывода ГРЗ
    # def get_queryset(self):
    #     application_id = self.kwargs.get('application_id')
    #     new_queryset = Application.objects.filter(
    #     application_id=application_id
    #     )
    #     return new_queryset
