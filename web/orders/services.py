from typing import Any

from django.db.models import Q
from django.db import transaction

from orders.models import OrderItem


@transaction.atomic
def create_order_item(**validated_data: dict[str, Any]) -> OrderItem:
    new_item_obj = OrderItem(**validated_data)

    same_product_items_qs = (
        OrderItem.objects.filter(order=new_item_obj.order)
        .filter(Q(bouquet=new_item_obj.bouquet) | Q(flower=new_item_obj.flower))
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
