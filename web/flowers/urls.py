from django.urls import path

from flowers import views

app_name = "flowers"

urlpatterns = [
    path("bouquets", views.BouquetListView.as_view(), name="bouquet_list"),
    path(
        "bouquets/category/<slug:slug>",
        views.BouquetCategoryDetailView.as_view(),
        name="bouquet_category_detail",
    ),
]
