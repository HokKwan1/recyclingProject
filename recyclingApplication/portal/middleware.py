from django.shortcuts import redirect
from django.contrib import messages
from django.utils.deprecation import MiddlewareMixin
import time 


# Redirect user to 
class Redirect404Middleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404  and not request.path.startswith('/admin'):
            print(request.path)
            messages.error(request, "Page Not Found 404")
            if (request.user.is_staff):
                return redirect("portal:dashboard")  # Redirect all 404s to home
            else:
                return redirect("portal:requests") 
            
        return response


# Middleware for loging user out after 10 mins of inactivity
class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get("last_activity")

            if last_activity:
                inactive_duration = time.time() - float(last_activity)
                if inactive_duration > 600: 
                    messages.error(request, "Session expired! Please login again.")
                    request.session.flush()  
                    return redirect("portal:portal_login")

            # Store timestamp instead of datetime
            request.session["last_activity"] = time.time()

        return self.get_response(request)
