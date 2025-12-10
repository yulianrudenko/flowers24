from pathlib import Path
from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


def get_bouquet_img_path(instance: "Bouquet", filename: str) -> str:
    ext = Path(filename).suffix
    new_filename = f"{uuid4()}{ext}"
    return str(Path("bouquets") / new_filename)


def get_flower_img_path(instance: "Flower", filename: str) -> str:
    ext = Path(filename).suffix
    new_filename = f"{uuid4()}{ext}"
    return str(Path("flowers") / new_filename)


class BaseProduct(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    MAX_ORDER_QUANTITY: int

    class Meta:
        abstract = True


class Flower(BaseProduct):
    image = models.ImageField(upload_to=get_flower_img_path)
    in_stock = models.BooleanField(default=True)
    can_be_sold_separately = models.BooleanField()

    MAX_ORDER_QUANTITY = 10_000

    class Meta:  # type: ignore
        verbose_name = _("Flower")
        verbose_name_plural = _("Flowers")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name}"


class BouquetCategory(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("flowers:bouquet-category-detail", args=[self.pk])


class Bouquet(BaseProduct):
    image = models.ImageField(upload_to=get_bouquet_img_path)
    categories = models.ManyToManyField(BouquetCategory, related_name="bouquets")
    flowers = models.ManyToManyField(
        Flower, through="BouquetFlower", related_name="bouquets"
    )

    MAX_ORDER_QUANTITY = 50

    class Meta:  # type: ignore
        verbose_name = _("Bouquet")
        verbose_name_plural = _("Bouquets")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name}"


class BouquetFlower(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE, related_name="bouquet_flowers")
    flower = models.ForeignKey(Flower, on_delete=models.PROTECT, related_name="bouquet_flowers")
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _("Bouquet Flower")
        verbose_name_plural = _("Bouquet Flowers")
        unique_together = ["bouquet", "flower"]
        ordering = ["bouquet"]

    def __str__(self):
        return f"{self.quantity} × {self.flower.name} in {self.bouquet.name}"
