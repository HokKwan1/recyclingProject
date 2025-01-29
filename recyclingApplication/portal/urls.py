from django.urls import path
from portal.views.views import *
from portal.views.dashboardView import DashboardView
from portal.views.authView import LoginView, LogoutView
from portal.views.volunteerView import AddVolunteerView, VolunteersView, VolunteerDetailsView
from portal.views.requestsView import RequestsView, RequestDetailsView, AvailableRequestView, ClaimRequestView, VolunteerRequestView

app_name = "portal"

urlpatterns = [
    path("login", LoginView.as_view(), name="portal_login"),
    path("home", HomeView.as_view(), name="portal_home"),
    path("logout", LogoutView.as_view(), name="portal_logout"),
    path("requests", RequestsView.as_view(), name="requests"),
    path("request-details/<int:id>", RequestDetailsView.as_view(), name="request_details"),
    path("request-available", AvailableRequestView.as_view(), name="request_available"),
    path("request-volunteer/<int:user_id>", VolunteerRequestView.as_view(), name="request_volunteer"),
    path("requests/claim/<int:request_id>/", ClaimRequestView.as_view(), name="claim_request"),
    path("volunteers", VolunteersView.as_view(), name="volunteers"),
    path("add-volunteer", AddVolunteerView.as_view(), name="add_volunteer"),
    path("volunteer-details/<int:id>", VolunteerDetailsView.as_view(), name="volunteer_details"),
    path("settings", SettingsView.as_view(), name="settings"),
    path("dashboard", DashboardView.as_view(), name="dashboard")
]
