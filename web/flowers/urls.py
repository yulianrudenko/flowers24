from django.urls import path

from flowers import views

app_name = "flowers"

urlpatterns = [
    path("flowers", views.FlowerListView.as_view(), name="flower-list"),
    path(
        "flowers/<uuid:pk>/",
        views.FlowerDetailView.as_view(),
        name="flower-detail",
    ),
    path("bouquets", views.BouquetListView.as_view(), name="bouquet-list"),
    path(
        "bouquets/<uuid:pk>/",
        views.BouquetDetailView.as_view(),
        name="bouquet-detail",
    ),
    path("categories", views.BouquetCategoryListView.as_view(), name="bouquet-category-list"),
    path(
        "categories/<uuid:pk>/",
        views.BouquetCategoryDetailView.as_view(),
        name="bouquet-category-detail",
    ),
]
