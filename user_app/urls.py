from django.urls import path
from .views import UserRegisterView, UserLoginView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)  # Import built-in view for refreshing tokens

urlpatterns = [
    path(
        "register/", UserRegisterView.as_view(), name="register"
    ),  # Endpoint for user registration
    path("login/", UserLoginView.as_view(), name="login"),  # Endpoint for user login
    path(
        "refresh-token/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # Endpoint to refresh access token
]
