from decimal import Decimal
from typing import Iterable
from uuid import uuid4

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from users.models import User
from flowers.models import Bouquet, Flower


class Order(models.Model):
    class Status(models.TextChoices):
        WAITING_PAYMENT = "waiting_payment", _("Waiting for payment")
        PAID = "paid", _("Paid")
        PREPARING = "preparing", _("Preparing")
        IN_DELIVERY = "in_delivery", _("In Delivery")
        DELIVERED = "delivered", _("Delivered")
        CANCELLED = "cancelled", _("Cancelled")
        REFUNDED = "refunded", _("Refunded")

    class DeliveryMethod(models.TextChoices):
        COURIER = "courier", _("Courier")
        PICKUP = "pickup", _("Self-pickup")

    postal_code_validator = RegexValidator(
        regex=r"^\d{2}-\d{3}$", message=_("Postal code must be in the format NN-NNN.")
    )

    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="orders", blank=False, null=True
    )
    status = models.CharField(
        max_length=20, choices=Status, default=Status.WAITING_PAYMENT.value
    )
    delivery_method = models.CharField(
        max_length=20, choices=DeliveryMethod, blank=True, null=True
    )
    notes = models.TextField(blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(
        max_length=6, blank=True, null=True, validators=[postal_code_validator]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Order")
        ordering = ["-created_at", "-updated_at"]

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    @property
    def total_price(self) -> Decimal:
        total = Decimal(0)
        for item in self.items.all():
            total += item.price

        return total


class OrderItem(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", null=False, blank=False
    )
    flower = models.ForeignKey(
        Flower,
        on_delete=models.CASCADE,
        related_name="order_items",
        blank=True,
        null=True,
    )
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.CASCADE,
        related_name="order_items",
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        constraints = [
            models.CheckConstraint(
                check=(models.Q(flower__isnull=True) | models.Q(bouquet__isnull=True)),
                name="no_both_flower_and_bouquet",
            )
        ]
        ordering = ["order"]

    @property
    def product_type(self) -> str:
        if self.flower is not None:
            return "flower"
        return "bouquet"

    @property
    def product(self) -> Flower | Bouquet | None:
        return self.flower or self.bouquet

    @property
    def in_stock(self) -> bool:
        if self.flower is not None:
            return self.flower.in_stock
        if self.bouquet is not None:
            return not self.bouquet.flowers.filter(in_stock=False).exists()

        return False

    @property
    def price(self) -> Decimal:
        if self.product is None:
            return Decimal(0)

        return self.product.price * self.quantity

    def __str__(self) -> str:
        if self.product is not None:
            return f"{self.quantity} × {self.product}"
        return _("unknown")

    def clean(self) -> None:
        super().clean()

        if self.flower and self.bouquet:
            raise ValidationError(_("Only one of flower or bouquet can be selected"))
        if not self.flower and not self.bouquet:
            raise ValidationError(
                {
                    "flower": _("You must select either flower or bouquet"),
                    "bouquet": _("You must select either flower or bouquet"),
                }
            )

        if self.product is not None and self.quantity > self.product.MAX_ORDER_QUANTITY:
            raise ValidationError(
                {
                    "quantity": _(
                        f"Maximum quantity for this product is {self.product.MAX_ORDER_QUANTITY}."
                    )
                }
            )

        if self.flower is not None and not self.flower.can_be_sold_separately:
            raise ValidationError(
                {"flower": _("This flower can not be sold separately from bouquet")}
            )


class Payment(models.Model):
    class Method(models.TextChoices):
        BLIK = "blik", "BLIK"
        PAYPAL = "paypal", "Paypal"

    class Status(models.TextChoices):
        PENDING = "pending", _("Pending")
        COMPLETED = "completed", _("Completed")
        FAILED = "failed", _("Failed")

    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="payments")
    method = models.CharField(max_length=30, choices=Method)
    status = models.CharField(
        max_length=20,
        choices=Status,
        default=Status.PENDING.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
