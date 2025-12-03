from rest_framework import serializers

from flowers.models import Bouquet, BouquetCategory, Flower


class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = ["id", "image", "in_stock", "allowed_to_sell_as_single", "bouquets"]


class BouquetSerializer(serializers.ModelSerializer):
    class BouquetCategoryInlineSerializer(serializers.ModelSerializer):
        bouquet_count = serializers.SerializerMethodField()

        class Meta:
            model = BouquetCategory
            fields = ["id", "name", "bouquet_count"]

        def get_bouquet_count(self, obj: BouquetCategory) -> int:
            return obj.bouquets.count()

    categories = BouquetCategoryInlineSerializer(
        many=True,
        read_only=True,
    )
    flowers = FlowerSerializer(many=True, read_only=True)

    class Meta:
        model = Bouquet
        fields = [
            "id",
            "name",
            "price",
            "description",
            "created_at",
            "image",
            "categories",
            "flowers",
        ]


class BouquetCategorySerializer(serializers.ModelSerializer):
    bouquets = BouquetSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = BouquetCategory
        fields = ["id", "name", "bouquets"]
