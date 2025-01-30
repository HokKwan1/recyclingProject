from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from portal.forms import CustomPasswordResetForm

class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'portal/settings.html')


class CustomPasswordResetView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordResetForm
    template_name = "portal/settings.html"
    success_url = reverse_lazy("portal:settings")  # Redirect after success
    def dispatch(self, request, *args, **kwargs):
        print("CustomPasswordResetView called!")  # Debugging
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)  # Keep user logged in
        messages.success(self.request, "Your password has been successfully updated!")

        print("Password updated successfully!")  # Debugging
        return response
