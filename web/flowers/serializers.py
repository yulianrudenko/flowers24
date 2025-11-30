from rest_framework import serializers

from flowers.models import Bouquet, BouquetCategory, Flower


class FlowerSerializer(serializers.HyperlinkedModelSerializer):
    bouquets = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="flowers:bouquet-detail", lookup_field="pk"
    )

    class Meta:
        model = Flower
        fields = ["id", "image", "in_stock", "allowed_to_sell_as_single", "bouquets"]


class BouquetCategorySerializer(serializers.ModelSerializer):
    bouquet_count = serializers.SerializerMethodField()

    class Meta:
        model = BouquetCategory
        fields = "__all__"

    def get_bouquet_count(self, obj: BouquetCategory) -> int:
        return obj.bouquets.count()


class BouquetSerializer(serializers.HyperlinkedModelSerializer):
    categories = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name="flowers:bouquet-category-detail",
        lookup_field="pk",
    )
    flowers = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="flowers:flower-detail", lookup_field="pk"
    )

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
