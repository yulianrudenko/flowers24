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
    queryset = Bouquet.objects.all()
    serializer_class = BouquetSerializer


class BouquetDetailView(RetrieveAPIView):
    queryset = Bouquet.objects.all()
    serializer_class = BouquetSerializer


class BouquetCategoryListView(ListAPIView):
    queryset = BouquetCategory.objects.all()
    serializer_class = BouquetCategorySerializer


class BouquetCategoryDetailView(RetrieveAPIView):
    queryset = BouquetCategory.objects.all()
    serializer_class = BouquetCategorySerializer
