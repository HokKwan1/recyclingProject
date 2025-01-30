from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator

from homepage.models import Request
from portal.filters import RequestFilter
from portal.services.google_services import get_coordinates


class BaseRequestView(LoginRequiredMixin, View):
    # Base view to handle login redirection and filtering logic.
    login_url = 'portal:portal_login'
    title = "Requests"

    def handle_no_permission(self):
        messages.error(self.request, 'You must be logged in to view this page.')
        return redirect(self.get_login_url())

    def filter_and_paginate(self, request, queryset, default_sort='-date_created'):
        # Applies filters, sorting, and pagination to a request queryset.
        filter_set = RequestFilter(request.GET, queryset=queryset)
        sorted_requests = filter_set.qs.order_by(request.GET.get('sort_by', default_sort))
        paginator = Paginator(sorted_requests, 7)
        return paginator.get_page(request.GET.get('page')), filter_set

    def render_request_page(self, request, requests, filter_set):
        return render(request, 'portal/requests/requests.html', {
            'requests': requests,
            'filter': filter_set,
            'title': self.title
        })


class RequestsView(BaseRequestView):
    # View for all requests based on user role.
    title = "All"

    def get(self, request):
        request_list = Request.objects.all() if request.user.is_staff else Request.objects.filter(claimed_by=request.user.id)
        requests, filter_set = self.filter_and_paginate(request, request_list)
        return self.render_request_page(request, requests, filter_set)


class RequestDetailsView(LoginRequiredMixin, View):
    # View for displaying request details with map coordinates.
    login_url = 'portal:portal_login'

    def get(self, request, id):
        req = get_object_or_404(Request, id=id)
        address = f'{req.address} {req.city} {req.state} {req.country} {req.postal_code}'
        locations = get_coordinates(address)
        return render(request, 'portal/requests/request_details.html', {'request': req, 'locations': locations})


class RestrictedVolunteerView(BaseRequestView):
    # Base view restricting staff from accessing volunteer-related pages.
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            messages.error(request, "You do not have permission to access this page.")
            return redirect("portal:dashboard")
        return super().dispatch(request, *args, **kwargs)


class AvailableRequestView(RestrictedVolunteerView):
    # View for listing available (pending) requests.
    title = "Available"

    def get(self, request):
        requests, filter_set = self.filter_and_paginate(request, Request.objects.filter(status='pending'))
        return self.render_request_page(request, requests, filter_set)


class VolunteerRequestView(RestrictedVolunteerView):
    # View for listing requests claimed by the logged-in volunteer.
    title = "Claimed"

    def get(self, request, user_id):
        requests, filter_set = self.filter_and_paginate(request, Request.objects.filter(claimed_by=user_id), 'status')
        return self.render_request_page(request, requests, filter_set)


class ClaimRequestView(LoginRequiredMixin, View):
    # View for handling request claiming by volunteers.
    login_url = 'portal:portal_login'

    def post(self, request, request_id):
        req = get_object_or_404(Request, id=request_id)

        if req.claimed_by:
            messages.warning(request, "This request has already been claimed.")
        else:
            claimed_requests = Request.objects.all().filter(claimed_by=request.user.id).filter(status='in_progress')
            if claimed_requests.__len__() >= 5:
                messages.error(request,  "You have claimed too many requests.")
            else:
                req.claimed_by = request.user
                req.status = "in_progress"
                req.save()
                messages.success(request, "You have successfully claimed the request.")

        return redirect("portal:request_available")
    
class CompleteRequestView(BaseRequestView):
    # View for handling request completion by volunteers.
    login_url = 'portal:portal_login'

    def post(self, request, request_id):
        req = get_object_or_404(Request, id=request_id)
        req.status = "completed"
        req.save()
        messages.success(request, "You have successfully completed the request.")
        url = reverse("portal:request_volunteer", kwargs={"user_id": request.user.id}) + "?status=in_progress"
        return HttpResponseRedirect(url)
        
