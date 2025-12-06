from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import (
    UserDetailAPIView,
    UserProfileAPIView,
    UserRegisterAPIView,
)

app_name = "users"

urlpatterns = [
    path("", UserRegisterAPIView.as_view(), name="register"),
    path("profile/", UserProfileAPIView.as_view(), name="profile"),
    path("<uuid:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token-refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
