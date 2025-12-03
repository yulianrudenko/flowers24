from django.urls import path

from flowers import views

app_name = "flowers"

urlpatterns = [
    path("flowers", views.FlowerListAPIView.as_view(), name="flower-list"),
    path(
        "flowers/<uuid:pk>/",
        views.FlowerDetailAPIView.as_view(),
        name="flower-detail",
    ),
    path("bouquets", views.BouquetListAPIView.as_view(), name="bouquet-list"),
    path(
        "bouquets/<uuid:pk>/",
        views.BouquetDetailAPIView.as_view(),
        name="bouquet-detail",
    ),
    path("categories", views.BouquetCategoryListAPIView.as_view(), name="bouquet-category-list"),
    path(
        "categories/<uuid:pk>/",
        views.BouquetCategoryDetailAPIView.as_view(),
        name="bouquet-category-detail",
    ),
]
