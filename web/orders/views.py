from rest_framework.generics import ListAPIView, RetrieveAPIView

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer


class OrderListView(ListAPIView):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer


class OrderItemDetailView(RetrieveAPIView):
    queryset = OrderItem.objects.select_related("order").all()
    serializer_class = OrderItemSerializer
