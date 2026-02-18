from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import farmer_report, home, login_view

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("report/farmer/", farmer_report, name="farmer_report"),
]
