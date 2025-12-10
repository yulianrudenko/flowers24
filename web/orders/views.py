from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order, OrderItem
from orders.serializers import OrderItemSerializer, OrderSerializer, PaymentSerializer
from orders.services import complete_order_payment


class OrderListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):  # type: ignore
        return Order.objects.prefetch_related("items").filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        empty_order = (
            request.user.orders.filter(status=Order.Status.WAITING_PAYMENT)
            .annotate(item_count=Count("items"))
            .filter(item_count=0)
            .first()
        )

        if empty_order:
            serializer = self.get_serializer(empty_order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return super().create(request, *args, **kwargs)


class OrderDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):  # type: ignore
        return Order.objects.prefetch_related("items").filter(user=self.request.user)


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


class OrderPayAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):  # type: ignore
        return Order.objects.prefetch_related("items").filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment = complete_order_payment(order, serializer.validated_data["method"])
        serializer = self.get_serializer(payment)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
