# middleware.py

from django.utils import timezone
from django.contrib.sessions.models import Session
from datetime import timedelta
from django.conf import settings
from django.shortcuts import redirect




class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and the session is not a new one
        if request.user.is_authenticated and 'last_activity' in request.session:
            last_activity = request.session['last_activity']

            # Calculate the elapsed time since the last activity
            elapsed_time = timezone.now() - last_activity

            # Set the session expiration to SESSION_COOKIE_AGE if the elapsed time exceeds it
            if elapsed_time > timedelta(seconds=settings.SESSION_COOKIE_AGE):
                Session.objects.filter(session_key=request.session.session_key).delete()
                request.session.flush()
                request.session['last_activity'] = timezone.now()

                return redirect('login')

      

        response = self.get_response(request)
        return response
#i did more configuration in the settings.py for this middleware to work
    #this was a test no more a test