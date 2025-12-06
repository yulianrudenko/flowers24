from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer, OrderSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from users.permissions import IsAuthenticated


class OrderListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):  # type: ignore
        return Order.objects.prefetch_related("items").filter(user=self.request.user)


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):  # type: ignore
        order_id = self.kwargs.get("order_id")
        return Order.objects.prefetch_related("items").filter(
            order_id=order_id, user=self.request.user
        )


class OrderItemListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):  # type: ignore
        order_id = self.kwargs.get("order_id")
        return OrderItem.objects.select_related("order").filter(
            order_id=order_id, order__user=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "order_id": self.kwargs.get("order_id"),
                "item_id": self.kwargs.get("item_id"),
            }
        )
        return context


class OrderItemDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):  # type: ignore
        order_id = self.kwargs.get("order_id")
        return OrderItem.objects.select_related("order").filter(
            order_id=order_id, order__user=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "order_id": self.kwargs.get("order_id"),
                "item_id": self.kwargs.get("item_id"),
            }
        )
        return context
