from django.http import HttpResponse, HttpResponseRedirect
from portal.forms import LoginForm
from django.views import View
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Handles user login via GET and POST requests.
# - GET: Displays the login form.
# - POST: Authenticates the user and redirects based on their role.


class LoginView(View):

    # Handles GET request.
    # - Renders the login page with an empty login form.
    def get(self, request):
        form = LoginForm

        return render(request, 'portal/login.html', {
            'loginForm': form
        })

    # Handles POST request.
    # - Validates login credentials.
    # - Authenticates user and logs them in.
    # - Redirects staff users to the dashboard and non-staff users to the requests page.
    # - Displays error messages for invalid login attempts.

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
                    request.session['user_id'] = user.id

                    if user.is_staff:
                        return HttpResponseRedirect(reverse('portal:dashboard'))
                    else:
                        return HttpResponseRedirect(reverse('portal:requests'))

                else:
                    messages.error(self.request, "Account is not active")
                    return HttpResponse('Account is not active')
            else:
                messages.error(
                    self.request, "Auth Error! Username and password don't match")
                return render(request, 'portal/login.html', {
                    'loginForm': form
                })
        else:
            messages.error(
                self.request, "Unknown Error! Please try again later")
            return render(request, 'portal/login.html', {
                'loginForm': form
            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        redirectPath = reverse('portal:portal_login')
        return HttpResponseRedirect(redirectPath)
