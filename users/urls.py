from django.urls import path
from .views import LoginAPIView, TokenRefreshAPIView

urlpatterns = [
    path("api/auth/login", LoginAPIView.as_view(), name="api-login"),
    path(
        "api/auth/token/refresh",
        TokenRefreshAPIView.as_view(),
        name="api-token-refresh",
    ),
]
