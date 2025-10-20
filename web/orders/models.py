from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User
from flowers.models import Bouquet, Flower


class Order(models.Model):
    class Status(models.TextChoices):
        WAITING_PAYMENT = "waiting_payment", _("Waiting for payment")
        PAID = "paid", _("Paid")
        PREPARING = "preparing", _("Preparing")
        IN_DELIVERY = "in_delivery", _("In Delivery")
        DELIVERY = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status, default=Status.WAITING_PAYMENT.value)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    @property
    def total_price(self) -> Decimal:
        total = Decimal(0)
        for item in self.items.all():
            total += item.price

        return total


class OrderItem(models.Model):
    class ProductType(models.TextChoices):
        FLOWER = "flower", _("Flower")
        BOUQUETE = "bouquete", _("Bouquete")

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_type = models.CharField(max_length=30, choices=ProductType)
    product_id = models.UUIDField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} × {self.product_type} (ID {self.product_id})"

    @property
    def price(self) -> Decimal:
        if self.product_type == self.ProductType.BOUQUETE.value:
            ProductCls = Bouquet
        elif self.product_type == self.ProductType.FLOWER.value:
            ProductCls = Flower
        else:
            return Decimal(0)

        try:
            product = ProductCls.objects.get(pk=self.product_id)
        except ProductCls.DoesNotExist:
            return Decimal(0)

        return product.price * self.quantity
