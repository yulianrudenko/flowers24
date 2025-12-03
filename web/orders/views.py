from rest_framework.generics import ListAPIView, RetrieveAPIView

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer


class OrderDetailAPIView(RetrieveAPIView):
    queryset = Order.objects.prefetch_related("items").all()
    serializer_class = OrderSerializer


class OrderItemDetailAPIView(RetrieveAPIView):
    queryset = OrderItem.objects.select_related("order").all()
    serializer_class = OrderItemSerializer
