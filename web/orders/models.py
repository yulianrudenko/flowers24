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
    postal_code_validator = RegexValidator(
        regex=r'^\d{2}-\d{3}$',
        message=_("Postal code must be in the format NN-NNN.")
    )

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

    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)
    status = models.CharField(
        max_length=20, choices=Status, default=Status.WAITING_PAYMENT.value
    )
    delivery_method = models.CharField(
        max_length=20, choices=DeliveryMethod, blank=False, null=False
    )
    notes = models.TextField(blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(
        max_length=6,
        validators=[postal_code_validator]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    items: models.QuerySet["OrderItem"]

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
    flower = models.ForeignKey(Flower, on_delete=models.SET_NULL, blank=True, null=True)
    bouquet = models.ForeignKey(
        Bouquet, on_delete=models.SET_NULL, blank=True, null=True
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
        if self.flower:
            return "flower"
        if self.bouquet:
            return "bouquet"
        return "unknown"

    @property
    def product(self) -> Flower | Bouquet | None:
        return self.flower or self.bouquet

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
