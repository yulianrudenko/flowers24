from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("", views.OrderListView.as_view(), name="order-list"),
    path(
        "<uuid:pk>/",
        views.OrderDetailView.as_view(),
        name="order-detail",
    ),
    path(
        "<uuid:order_id>/items/<uuid:pk>/",
        views.OrderItemDetailView.as_view(),
        name="order-item-detail",
    ),
]
