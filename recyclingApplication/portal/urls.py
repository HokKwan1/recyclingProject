from django.urls import path
from portal.views.views import *
from portal.views.dashboardView import DashboardView
from portal.views.authView import LoginView, LogoutView

app_name = "portal"

urlpatterns = [
    path("login", LoginView.as_view(), name="portal_login"),
    path("home", HomeView.as_view(), name="portal_home"),
    path("logout", LogoutView.as_view(), name="portal_logout"),
    path("requests", RequsetsView.as_view(), name="requests"),
    path("volunteers", VolunteersView.as_view(), name="volunteers"),
    path("add-volunteer", AddVolunteerView.as_view(), name="add_volunteer"),
    path("settings", SettingsView.as_view(), name="settings"),
    path("dashboard", DashboardView.as_view(), name="dashboard")
]
