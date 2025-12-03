from decimal import Decimal
from uuid import uuid4

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
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

    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status, default=Status.WAITING_PAYMENT.value
    )
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    items: models.QuerySet["OrderItem"]

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    @property
    def total_price(self) -> Decimal:
        total = Decimal(0)
        for item in self.items.all():
            total += item.price

        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    flower = models.ForeignKey(Flower, null=True, blank=True, on_delete=models.SET_NULL)
    bouquet = models.ForeignKey(
        Bouquet, null=True, blank=True, on_delete=models.SET_NULL
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )

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
        if self.flower and self.bouquet:
            raise ValidationError(_("Only one of flower or bouquet can be selected"))
        if not self.flower and not self.bouquet:
            raise ValidationError(_("You must select either flower or bouquet"))

        if self.product is not None and self.quantity > self.product.MAX_ORDER_QUANTITY:
            raise ValidationError(
                _(
                    f"Maximum quantity for this product is {self.product.MAX_ORDER_QUANTITY}."
                )
            )
