from django.contrib import admin

from flowers.models import (
    Bouquet,
    BouquetCategory,
    BouquetFlower,
    Flower,
)


class BouquetFlowerInline(admin.TabularInline):
    model = BouquetFlower
    extra = 1


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [BouquetFlowerInline]


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    pass


@admin.register(BouquetCategory)
class BouquetCategoryAdmin(admin.ModelAdmin):
    pass
