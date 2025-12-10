from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("", views.OrderListAPIView.as_view(), name="order-list"),
    path(
        "<uuid:pk>/",
        views.OrderDetailAPIView.as_view(),
        name="order-detail",
    ),
    path(
        "<uuid:order_id>/items/",
        views.OrderItemListAPIView.as_view(),
        name="order-item-list",
    ),
    path(
        "<uuid:order_id>/items/<uuid:pk>/",
        views.OrderItemDetailAPIView.as_view(),
        name="order-item-detail",
    ),
    path(
        "<uuid:pk>/pay/",
        views.OrderPayAPIView.as_view(),
        name="order-pay",
    ),
]
