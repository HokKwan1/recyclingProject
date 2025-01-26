from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth.models import User as AuthUser
from homepage.models import Request

from django.shortcuts import render
from portal.forms import VolunteerForm

from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Q

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
        return render(request, 'portal/volunteers/volunteers.html', {
            'volunteers': volunteers
        })
    
class AddVolunteerView(LoginRequiredMixin, View):
    def get(self, request):
        form = VolunteerForm()
        return render(request, 'portal/volunteers/add_volunteer.html', {'form': form})

    def post(self, request):
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New volunteer added successfully!")
            return redirect('portal:volunteers')  # Redirect to volunteer list page
        else:
            messages.error(request, "Error adding volunteer. Please check the details.")
            return render(request, 'portal/volunteers/add_volunteer.html', {'form': form})

class VolunteerDetailsView(LoginRequiredMixin, View):
    def get(self, request, id):
        volunteer = AuthUser.objects.get(id=id)
        requests = Request.objects.all().filter(claimed_by=volunteer)
        print(requests)
        return render(request, 'portal/volunteers/volunteer_details.html', {
            'volunteer': volunteer,
            'requests': requests
        })