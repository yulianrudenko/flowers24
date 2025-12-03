from rest_framework.generics import ListAPIView, RetrieveAPIView

from flowers.models import Flower, Bouquet, BouquetCategory
from flowers.serializers import (
    BouquetSerializer,
    BouquetCategorySerializer,
    FlowerSerializer,
)


class FlowerListView(ListAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer


class FlowerDetailView(RetrieveAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer


class BouquetListView(ListAPIView):
    queryset = Bouquet.objects.prefetch_related("flowers").all()
    serializer_class = BouquetSerializer


class BouquetDetailView(RetrieveAPIView):
    queryset = Bouquet.objects.prefetch_related("flowers").all()
    serializer_class = BouquetSerializer


class BouquetCategoryListView(ListAPIView):
    queryset = BouquetCategory.objects.prefetch_related("bouquets").all()
    serializer_class = BouquetCategorySerializer


class BouquetCategoryDetailView(RetrieveAPIView):
    queryset = BouquetCategory.objects.prefetch_related("bouquets").all()
    serializer_class = BouquetCategorySerializer
