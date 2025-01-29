from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from portal.services.highchart_services import *

class DashboardView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("portal:requests")  # Redirect non-staff users to requests page
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request):
        count_data = createCityCountChart()
        chart_data = createCityCountBreakdownChart()
        user_status_data = createActiveUserChart()
        volunteer_ranking = createVolunteerRankingChart()
        latest_joined_volunteer = createLatestJoinVolunteerData()
        latest_submitted_Request = createLatestSubmittedRequestData()

        return render(request, "portal/dashboard.html", {
            'chart_data': chart_data,
            'count_data': count_data,
            'user_status_data': user_status_data ,
            'volunteer_ranking' : volunteer_ranking,
            'latest_joined_volunteer': latest_joined_volunteer,
            'latest_submitted_Request': latest_submitted_Request
        })

def createLatestJoinVolunteerData():
    volunteers = AuthUser.objects.all().filter(
            is_staff=False).order_by('-date_joined')[:5]
    
    return volunteers

def createLatestSubmittedRequestData():
    requests = Request.objects.all().filter(status='pending').order_by('-date_created')[:5]
    
    return requests
