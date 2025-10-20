from uuid import uuid4

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class BaseProduct(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, db_index=True
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Flower(BaseProduct):
    stock = models.PositiveIntegerField(default=0)  # TODO: subtract qty when ordering
    allowed_to_sell_as_single = models.BooleanField()

    def __str__(self) -> str:
        return f"{self.name}"


class BouquetCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("flowers:bouquet_category_detail", args=[self.slug])


class Bouquet(BaseProduct):
    flowers = models.ManyToManyField(
        Flower, through="BouquetFlower", related_name="bouquets"
    )
    categories = models.ManyToManyField(BouquetCategory, related_name="bouquets")

    def __str__(self) -> str:
        return f"{self.name}"


class BouquetFlower(models.Model):
    bouquet = models.ForeignKey(Bouquet, on_delete=models.CASCADE)
    flower = models.ForeignKey(Flower, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ["bouquet", "flower"]

    def __str__(self):
        return f"{self.quantity} × {self.flower.name} in {self.bouquet.name}"
