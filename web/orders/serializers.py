from django.core.exceptions import ValidationError
from rest_framework import serializers

from orders import services
from orders.models import Order, OrderItem, Payment
from flowers.serializers import FlowerSerializer, BouquetSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "method",
            "status",
            "created_at",
            "completed_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "order": {"read_only": True},
            "status": {"read_only": True},
            "created_at": {"read_only": True},
            "completed_at": {"read_only": True},
        }


class BaseOrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "flower",
            "bouquet",
            "product",
            "quantity",
        ]

    def get_product(self, obj):
        if obj.flower is not None:
            return FlowerSerializer(obj.flower, context=self.context).data
        if obj.bouquet is not None:
            return BouquetSerializer(obj.bouquet, context=self.context).data

        return None


class OrderItemListSerializer(BaseOrderItemSerializer):
    class Meta(BaseOrderItemSerializer.Meta):
        read_only_fields = ["order"]

    def to_internal_value(self, data):
        attrs = super().to_internal_value(data)

        if self.instance is None:
            if (order_id := self.context.get("order_id")) is None:
                raise ValueError("No order ID in context")
            attrs["order_id"] = order_id

        return attrs

    def validate(self, attrs):
        obj = OrderItem(**attrs)

        try:
            obj.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs

    def create(self, validated_data: dict) -> OrderItem:
        return services.create_order_item(**validated_data)


class OrderItemDetailSerializer(BaseOrderItemSerializer):
    product = serializers.SerializerMethodField(read_only=True)

    class Meta(BaseOrderItemSerializer.Meta):
        read_only_fields = [
            "order",
            "flower",
            "bouquet",
            "product",
        ]

    def validate(self, attrs):
        obj: OrderItem = self.instance  # type: ignore
        for field, value in attrs.items():
            setattr(obj, field, value)

        try:
            obj.full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)

        return attrs

    def update(self, instance: OrderItem, validated_data):
        if instance.order.status not in [
            Order.Status.WAITING_PAYMENT,
            Order.Status.PAID,
            Order.Status.PREPARING,
        ]:
            return
        return super().update(instance, validated_data)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "delivery_method",
            "notes",
            "address_line1",
            "address_line2",
            "city",
            "postal_code",
            "items",
            "total_price",
            "payments",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
            "status": {"read_only": True},
            "delivery_method": {"required": False, "allow_blank": False},
            "notes": {"read_only": True},
            "city": {"required": False, "allow_blank": False},
            "postal_code": {"required": False, "allow_blank": False},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, attrs) -> dict:
        if (user := getattr(self.context.get("request", None), "user", None)) is None:
            raise ValueError("No info about request user")

        try:
            Order(**attrs, user=user).full_clean(exclude="user")
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return attrs

    def create(self, validated_data: dict) -> Order:
        order = Order(**validated_data)
        order.user = self.context["request"].user
        order.save()
        return order
