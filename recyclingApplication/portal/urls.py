from django.urls import path
from . import views

app_name = "portal"

urlpatterns = [
    path("login", views.LoginView.as_view(), name="portal_login"),
    path("home", views.HomeView.as_view(), name="portal_home"),
    path("logout", views.LogoutView.as_view(), name="portal_logout"),
    path("requests", views.RequsetsView.as_view(), name="requests"),
    path("volunteers", views.VolunteersView.as_view(), name="volunteers"),
    path("settings", views.SettingsView.as_view(), name="settings"),
    path("dashboard", views.DashboardView.as_view(), name="dashboard"),
]
