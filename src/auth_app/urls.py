from django.urls import path

from .views import LoginAPIView, LogoutAPIView, RegisterAPIView, TokenRefreshAPIView

urlpatterns = [
    path("register", RegisterAPIView.as_view(), name="auth_register"),
    path("login", LoginAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshAPIView.as_view(), name="token_refresh"),
    path("logout", LogoutAPIView.as_view(), name="auth_logout"),
]
