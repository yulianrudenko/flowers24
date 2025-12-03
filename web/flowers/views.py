from rest_framework.generics import ListAPIView, RetrieveAPIView

from flowers.models import Flower, Bouquet, BouquetCategory
from flowers.serializers import (
    BouquetSerializer,
    BouquetCategorySerializer,
    FlowerSerializer,
)


class FlowerListAPIView(ListAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer


class FlowerDetailAPIView(RetrieveAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer


class BouquetListAPIView(ListAPIView):
    queryset = Bouquet.objects.prefetch_related("flowers").all()
    serializer_class = BouquetSerializer


class BouquetDetailAPIView(RetrieveAPIView):
    queryset = Bouquet.objects.prefetch_related("flowers").all()
    serializer_class = BouquetSerializer


class BouquetCategoryListAPIView(ListAPIView):
    queryset = BouquetCategory.objects.prefetch_related("bouquets").all()
    serializer_class = BouquetCategorySerializer


class BouquetCategoryDetailAPIView(RetrieveAPIView):
    queryset = BouquetCategory.objects.prefetch_related("bouquets").all()
    serializer_class = BouquetCategorySerializer
