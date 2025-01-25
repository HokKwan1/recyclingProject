from django.http import HttpResponse
from django.shortcuts import render

from django.views import View
from django.core.paginator import Paginator

from homepage.models import Request

from django.contrib.auth.models import User as AuthUser
from portal.forms import VolunteerForm

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.


def index(request):
    return HttpResponse('temp')


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'portal/portal_home.html')


class RequsetsView(LoginRequiredMixin, View):
    login_url = 'portal:portal_login'

    def handle_no_permission(self):
        messages.error(
            self.request, 'You must be logged in to view this page.')
        return redirect(self.get_login_url())

    def get(self, request):
        if request.user.is_staff:
            request_list = Request.objects.all().order_by('id')
        else:
            request_list = Request.objects.all().filter(
                claimed_by=request.user.id).order_by('id')

        paginator = Paginator(request_list, 7)

        page_number = request.GET.get('page')
        requests = paginator.get_page(page_number)

        return render(request, 'portal/requests.html', {
            'requests': requests
        })


class VolunteersView(LoginRequiredMixin, View):
    def get(self, request):

        volunteer_list = AuthUser.objects.filter(is_staff=False).order_by(
            'id').prefetch_related('claimed_requests')
        for volunteer in volunteer_list:
            volunteer.completed_requests = volunteer.claimed_requests.filter(
                status='completed')
            volunteer.pending_requests = volunteer.claimed_requests.filter(
                Q(status='pending') | Q(status='in_progress'))

        paginator = Paginator(volunteer_list, 10)
        page_number = request.GET.get('page')
        volunteers = paginator.get_page(page_number)
        return render(request, 'portal/volunteers.html', {
            'volunteers': volunteers
        })
    
class AddVolunteerView(LoginRequiredMixin, View):
    def get(self, request):
        form = VolunteerForm()
        return render(request, 'portal/add_volunteer.html', {'form': form})

    def post(self, request):
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New volunteer added successfully!")
            return redirect('portal:volunteers')  # Redirect to volunteer list page
        else:
            messages.error(request, "Error adding volunteer. Please check the details.")
            return render(request, 'portal/add_volunteer.html', {'form': form})


class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'portal/settings.html')
