from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path("<int:month>", views.monthly_challenge_by_number),
    # Naming a path can be use in redirection
    # path("<str:month>", views.monthly_challenge, name='monthly_challenge'),
]
