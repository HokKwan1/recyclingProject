import secrets

from django.shortcuts import render
from django.views import View
from .forms import CreateRequestForm
from django.utils import timezone
from portal.services.email_services import EmailService

# Create your views here.

class IndexView(View):
    def get(self, request):
        form = CreateRequestForm()
        return render(request, "homepage/index.html", {
            "createRequestForm": form
        })

    def post(self, request):
        form = CreateRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.date_created = timezone.now().date()
            instance.status = "Pending"
            token = secrets.token_urlsafe(16)
            instance.token = token

            instance.save()

            email_service = EmailService()
            email_service.send_welcome_email(instance=instance)

            return render(request, "homepage/thank_you.html", {
                'token' : token
            })
        else:
            return render(request, "homepage/index.html", {
            "createRequestForm": form
        })

        # else:
            # Not using render here because render always return a success response.
            # we need to send the 404 error code along with the view
            # return render(request, "404.html")
            # return HttpResponseNotFound(render_to_string("404.html"))

            # Or you can raise a Http404, and it will automatically find the
            # 404.html in the root templates. Just make sure the filename is
            # 404.html. Require DEBUG=False to show the 404 page.
            # raise Http404()

    




