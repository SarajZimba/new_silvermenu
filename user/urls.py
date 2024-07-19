from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    logout_user,
)


app_name = "user"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login_view"),
    path("logout/", logout_user, name="logout"),
]