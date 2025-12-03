from django.core.exceptions import ValidationError
from rest_framework import serializers

from orders.models import Order, OrderItem
from flowers.serializers import FlowerSerializer, BouquetSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    flower = FlowerSerializer(read_only=True)
    bouquet = BouquetSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "flower", "bouquet", "quantity"]

    def validate(self, attrs):
        try:
            OrderItem(**attrs).full_clean()
        except ValidationError as e:
            raise serializers.ValidationError(e.message_dict)
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            # "user",
            "status",
            "notes",
            "items",
            "created_at",
            "updated_at",
        ]
