from django.shortcuts import redirect

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.profile.is_complete:
            return redirect('setup')  # Replace 'setup' with the URL name for profile setup
        response = self.get_response(request)
        return response


