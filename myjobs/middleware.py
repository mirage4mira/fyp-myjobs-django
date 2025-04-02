from django.shortcuts import redirect
from django.urls import reverse
from django.db import connection

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Authenticated: {request.user.is_authenticated}, User: {request.user}")
        # Skip middleware for unauthenticated users or specific paths
        if not request.user.is_authenticated or request.path in [reverse('setup_profile'), reverse('logout')]:
            return self.get_response(request)

        # Check if the user's user_profile entry exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM myjobs_userprofile WHERE user_id = %s", [request.user.id])
            result = cursor.fetchone()

        if not result:  # If user_profile entry does not exist
            return redirect('setup_profile')  # Redirect to profile setup page

        return self.get_response(request)
