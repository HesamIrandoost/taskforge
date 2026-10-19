from django.urls import path

from .views import RegisterView, LoginView, ProfileView, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "account"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
