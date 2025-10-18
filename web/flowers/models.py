from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseProduct(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True


class Flower(BaseProduct):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)
    allowed_to_sell_as_single = models.BooleanField(
        default=True,
        help_text="Can this flower be sold individually (not just in bouquets)"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name}"


class Bouquet(BaseProduct):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    flowers = models.ManyToManyField(
        Flower,
        through='BouquetFlower',
        related_name='bouquets'
    )

    def __str__(self) -> str:
        return f"{self.name}"


class BouquetFlower(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('bouquet', 'flower')

    def __str__(self):
        return f"{self.quantity} × {self.flower.name} in {self.bouquet.name}"
