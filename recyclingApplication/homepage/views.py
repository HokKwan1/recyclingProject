import secrets

from django.shortcuts import render
from django.views import View
from .forms import CreateRequestForm, RequestByTokenForm
from django.utils import timezone
from portal.services.email_services import EmailService
from homepage.models import Request

class IndexView(View):
    def get(self, request):
        create_form = CreateRequestForm()
        token_form = RequestByTokenForm()
        return render(request, "homepage/index.html", {
            "createRequestForm": create_form,
            "tokenForm": token_form
        })

    def post(self, request):
        create_form = CreateRequestForm(request.POST) if "request_create" in request.POST else CreateRequestForm()
        token_form = RequestByTokenForm(request.POST) if "request_lookup" in request.POST else RequestByTokenForm()

        # Handle request creation
        if "request_create" in request.POST:
            if create_form.is_valid():
                instance = create_form.save(commit=False)
                instance.date_created = timezone.now().date()
                instance.status = "pending"
                instance.token = secrets.token_urlsafe(16)

                instance.save()

                # Send email
                email_service = EmailService()
                email_service.send_welcome_email(instance=instance)

                return render(request, "homepage/thank_you.html", {
                    'token': instance.token
                })

        # Handle request lookup
        elif "request_lookup" in request.POST:
            if token_form.is_valid():
                token = token_form.cleaned_data["token"]
                request_obj = Request.objects.filter(token=token).first()

                if request_obj:
                    return render(request, "homepage/request_details.html", {
                        "request_obj": request_obj
                    })
                else:
                    token_form.add_error("token", "No request found with this token.")

        return render(request, "homepage/index.html", {
            "createRequestForm": create_form,
            "tokenForm": token_form
        })
