from typing import Any

from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError

from orders.models import Order, OrderItem, Payment


@transaction.atomic
def create_order_item(**validated_data: dict[str, Any]) -> OrderItem:
    new_item_obj = OrderItem(**validated_data)
    if not new_item_obj.in_stock:
        raise ValidationError({"detail": _("Currently product is not in stock")})

    same_product_items_qs = OrderItem.objects.filter(order=new_item_obj.order).filter(
        Q(bouquet=new_item_obj.bouquet) | Q(flower=new_item_obj.flower)
    )

    if same_product_items_qs.exists():
        item_obj = same_product_items_qs[0]
        for tmp_item_obj in same_product_items_qs[1:]:
            item_obj.quantity += tmp_item_obj.quantity

        item_obj.quantity += new_item_obj.quantity
        same_product_items_qs.exclude(pk=item_obj.pk).delete()
    else:
        item_obj = new_item_obj

    item_obj.save()
    return item_obj


@transaction.atomic
def complete_order_payment(
    order: Order, payment_methd: Payment.Method
) -> Payment | None:
    if order.status != Order.Status.WAITING_PAYMENT:
        raise ValidationError(
            {"detail": _("Order is already paid or cannot be paid")}
        )
    if not order.items.exists():
        raise ValidationError(
            {"detail": _("Cannot pay for empty order")}
        )
    if order.items.filter(
        Q(flower__in_stock=False) | Q(bouquet__flowers__in_stock=False)
    ).exists():
        raise ValidationError(
            {"detail": _("Currently one of the order products is not in stock")}
        )

    payment = Payment.objects.create(
        order=order,
        method=payment_methd,
        status=Payment.Status.COMPLETED,
        completed_at=timezone.now(),
    )

    order.status = Order.Status.PAID
    order.save(update_fields=["status"])

    return payment
