from django.contrib import admin

from flowers.models import (
    Flower,
    Bouquet,
    BouquetCategory
)


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    pass


@admin.register(BouquetCategory)
class BouquetCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Flower)
class FlowerAdmin(admin.ModelAdmin):
    pass
