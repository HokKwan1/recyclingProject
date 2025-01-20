from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .models import TestModel
from .forms import LoginForm

from homepage.models import Request

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as AuthUser, Group
from portal.services.email_services import EmailService

# Create your views here.


def index(request):
    return HttpResponse("temp")


class LoginView(View):
    def get(self, request):
        form = LoginForm

        return render(request, "portal/login.html", {
            "loginForm": form
        })

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['user_name'], password=data['password']
            )

            if user:
                if user.is_active:
                    login(request, user)
                    request.session["user_id"] = user.id

                    user_details = {
                        "last_name": user.last_name,
                        "first_name": user.first_name,
                    }
                    

                    return HttpResponseRedirect(reverse("portal:portal_home"))
                    # return HttpResponseRedirect(request.GET.get('redirec_to', '/portal/home'))
                else:
                    return HttpResponse("Account is not active")
            else:
                return render(request, 'portal/login.html', {
                    'loginForm': form
                })
        else:
            return render(request, 'portal/login.html', {
                'loginForm': form,
                'user': user_details
            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        redirectPath = reverse("portal:portal_login")
        return HttpResponseRedirect(redirectPath)


class HomeView(View):
    def get(self, request):
        return render(request, "portal/portal-home.html")


class RequsetsView(View):
    def get(self, request):
        requests = Request.objects.all()

        return render(request, "portal/requests.html", {
            "requests": requests
        })

class VolunteersView(View):
    def get(self, request):
        return render(request, "portal/volunteers.html")
    
class SettingsView(View):
    def get(self, request):
        return render(request, "portal/settings.html")
    
class DashboardView(View):
    def get(self, request):
        chart_data = {
        'chart': {
            'type': 'column'
        },
        'title': {
            'text': 'Monthly Sales'
        },
        'xAxis': {
            'categories': ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        },
        'yAxis': {
            'title': {
                'text': 'Sales'
            }
        },
        'series': [{
            'name': 'Sales',
            'data': [10, 15, 25, 30, 40]
        }]
    }
        return render(request, "portal/dashboard.html",{
            'chart_data': chart_data
        })
    