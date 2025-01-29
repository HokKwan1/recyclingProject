from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from django.core.paginator import Paginator

from homepage.models import Request

from django.contrib.auth.models import User as AuthUser


from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from portal.filters import RequestFilter

# Create your views here.


def index(request):
    return HttpResponse('temp')


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'portal/portal_home.html')


class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'portal/settings.html')
