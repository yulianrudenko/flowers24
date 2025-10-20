from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("flowers/", include("flowers.urls", namespace="flowers")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("users/", include("users.urls", namespace="users")),
]
