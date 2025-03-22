from django.shortcuts import render, redirect
from django.views import View
from portal.forms import AdminForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateUserView(View):
    template_name = "portal/create_user.html"

    def get(self, request):
        form = AdminForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully!")
            return redirect("portal:volunteers")  # Redirect to a suitable page
        else:
            return render(request, self.template_name, {"form": form})
